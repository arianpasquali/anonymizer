# %%
# Load required libraries
import re
from datetime import datetime
from datetime import date
from faker import Faker
#import spacy
import csv
import os
from nltk.tokenize import word_tokenize
import codecs

#spacy.cli.download("pt")
#python -m spacy download pt_core_news_sm

# %%
class Anonymization():
    def __init__(self,filename):
        self.filename = filename
        #elf.nlp_pt = spacy.load("pt")

    def detect_named_entities(self):
        doc = self.nlp_pt(self.ftext)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

    def hide_age_mentions(self):
        age_regex = r"(\d+)?.*?(anos)"
        result = re.sub(age_regex," XXX anos ", self.ftext)
        self.ftext = result

    def load_nomes_communs(self):
        self.nomes = []

        for file in os.listdir("./nomes_proprios"):
            if(file.endswith(".csv")):
                with open('nomes_proprios/' + file) as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        tmp_nome = row[0].strip()
                        if(len(tmp_nome) > 3):

                            self.nomes.append(tmp_nome)
            else:
                with open("nomes_proprios/"+ file) as txtfile:
                    tnomes = txtfile.readlines()
                    tnomes = [x.strip() for x in tnomes if len(x) > 3]
                    
                    self.nomes = self.nomes.extends(tnomes)


        self.nomes = list(set(self.nomes))        

    def standardize_dates(self):
        # dd/mm/yyyy  »  yyyy/mm/dd
        p = re.compile(r'(\d\d)[/|\.|-](\d\d)[/|\.|-](\d\d\d\d)')
        self.ftext = p.sub(r'\3-\2-\1', self.ftext)

        # dd/m/yyyy  »  yyyy/mm/dd
        p = re.compile(r'(\d\d)[/|\.|-](\d)[/|\.|-](\d\d\d\d)')
        self.ftext = p.sub(r'\3-0\2-\1', self.ftext)

        # d/mm/yyyy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d)[/|\.|-](\d\d)[/|\.|-](\d\d\d\d)')
        self.ftext = p.sub(r'\3-\2-0\1', self.ftext)

        # d/m/yyyy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d)[/|\.|-](\d)[/|\.|-](\d\d\d\d)')
        self.ftext = p.sub(r'\3-0\2-0\1', self.ftext)

        # dd/mm/yy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d\d)[/|\.|-](\d\d)[/|\.|-](\d\d)[\s|\.|,]')
        self.ftext = p.sub(r'20\3-\2-\1', self.ftext)

        # dd/m/yy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d\d)[/|\.|-](\d)[/|\.|-](\d\d)(\d\d)[\s|\.|,]')
        self.ftext = p.sub(r'20\3-0\2-\1', self.ftext)

        # d/mm/yy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d)[/|\.|-](\d\d)[/|\.|-](\d\d)[\s|\.|,]')
        self.ftext = p.sub(r'20\3-\2-0\1', self.ftext)

        # d/m/yy  »  yyyy/mm/dd
        p = re.compile(r'[\s|\.|,|:](\d)[/|\.|-](\d)[/|\.|-](\d\d)[\s|\.|,]')
        self.ftext = p.sub(r'20\3-0\2-0\1', self.ftext)


    def anonymizes_dates(self):
        # Standardize date's pattern
        self.standardize_dates()

        # Get dates
        date_pattern = re.compile(r'((\d+-\d+-\d+)(\s*\d+:\d+)?)')
        date_list = list() 
        format_str = '%Y-%m-%d' # The format
        format_str2 = '%d-%m-%Y' # The format
            
        # Using set 
        seen = set() 
        i = 0
        for m in re.finditer(date_pattern, self.ftext):
            try:
                # print(m.group(2),'\n\n')
                datetime_obj = datetime.strptime(m.group(2), format_str)
                if not (m.group(0) in seen or seen.add(m.group(0))):
                    date_list.append(((datetime_obj.date()), m.group(0), i))
                    i += 1
            except:
                try:                
                    datetime_obj = datetime.strptime(m.group(2), format_str2)
                    datetime_obj = datetime.strftime(datetime_obj,'%Y-%m-%d')
                    datetime_obj = datetime.strptime(datetime_obj, format_str)
                    if not (m.group(0) in seen or seen.add(m.group(0))):
                        date_list.append(((datetime_obj.date()), m.group(0), i))
                        i += 1
                except:
                    pass
            finally:
                pass

            # Sort dates
            date_list.sort(key=lambda x:x[0])
            # date_list

        try:
            # Replace dates for the pattern <<##date:delta##>>
            for d in date_list: 
                base = date(1980,1,1)
                delta =  d[0] - base
                # print(delta.days)
                p = re.compile('{}'.format(d[1]))
                self.ftext = p.sub(' <<##date:'+str(delta.days)+'##>> ', self.ftext)
        except:
            pass


    # Remove headers: also remove process number
    def remove_headers(self):
        p = re.compile(r'(Data:)(.*?)(Utilizador:\s?\w+)',re.DOTALL)
        self.ftext = p.sub('',self.ftext)


    def anonymizes_name(self, full_name_list, seed):
        fakerGenerator = Faker()
        fakerGenerator.random.seed(seed)
        last_names = [fakerGenerator.last_name() for i in range(len(full_name_list))]

        new_name = list()
        for i, n in enumerate(full_name_list):
            fakerGenerator.random.seed(seed)
            if i == 0:
                new_name.append((fakerGenerator.first_name(), n))
            else:
                new_name.append((last_names[i],n))
        return new_name
        

    def anonymizes_dr_names(self):
        # E.g: Dra. Dra. XX » Dra. XX
        p = re.compile(r'[\W](dr\.|dra\.?|Dr\.?|Dra\.?)\s(dr\.|dra\.?|Dr\.|Dra\.?)')
        self.ftext = p.sub('\1', self.ftext)

        p = re.compile(r'[\W](dr\.?|dra\.?|Dr\.?|Dra\.?|DR\.|DRA\.?)(\s+\w+)(\s[A-Z][a-z]+)*')
        for i, m in enumerate(re.finditer(p, self.ftext)):
            # print(m.group(),m.group().split()[1:])
            full_name_list = m.group().split()[1:]
            new_name = self.anonymizes_name(full_name_list, i)
            for i, x in enumerate(new_name):
                self.ftext = re.sub(f'{x[1]}|{x[1].lower()}|{x[1].upper()}|{x[1].title()}', x[0], self.ftext)

    
    def anonymizes_patient_name(self):
        # Get full name        
        full_name = re.search('\-(.+)?[Utilizador]',self.ftext)[0]
        full_name = re.sub('\s+Utilizador','', full_name).split('- ')[1]

        full_name_list = full_name.split()
        new_name = self.anonymizes_name(full_name_list,2020)
        for i, x in enumerate(new_name):
            self.ftext = re.sub(f'{x[1]}|{x[1].lower()}|{x[1].upper()}|{x[1].title()}', x[0], self.ftext)


    def anonymizes_commmon_names(self):
        #self.nomes
        fakerGenerator = Faker()
        fakerGenerator.random.seed(123)

        tmp_text = self.ftext.replace("\t","<TAB>").replace("  ","<SPACE>").replace("\n\n","<BREAKLINE>")
        lines = tmp_text.split("\n")
        
        for idl, line in enumerate(lines):
            if(len(line) <= 3):
                continue

            tokens = word_tokenize(line)

            for idx, ftoken in enumerate(tokens):
                if(ftoken.isdigit() or len(ftoken) <= 3):
                    continue
                if(ftoken in self.nomes):
                    if(ftoken in ["Marco"]):
                        continue
                    new_name = fakerGenerator.first_name()

                    # new_name = self.nomes[self.nomes.index(ftoken)+1]
                    print("anonymizes",idx, ftoken, "replace for",new_name) 
                    tokens[idx] =  new_name                

            lines[idl] = " ".join(tokens)

        tmp_text = "\n".join(lines)
        tmp_text = tmp_text.replace("< TAB >","\t").replace("< SPACE >","  ").replace("< BREAKLINE >","\n\n")
        self.ftext = tmp_text
        # self.ftext = "\n".join(lines)
        # p = re.compile(r'(D.ª(\s+\w+)(\s[A-Z][a-z]+)*)')
        # for i, m in enumerate(re.finditer(p, self.ftext)):
        #     full_name_list = m.group().split()[1:]
        #     new_name = self.anonymizes_name(full_name_list, 50-i)
        #     for i, x in enumerate(new_name):
        #         self.ftext = re.sub(f'{x[1]}|{x[1].lower()}|{x[1].upper()}|{x[1].title()}', x[0], self.ftext)


    def anonymizes_other_names(self):

        p = re.compile(r'(D.ª(\s+\w+)(\s[A-Z][a-z]+)*)')
        for i, m in enumerate(re.finditer(p, self.ftext)):
            full_name_list = m.group().split()[1:]
            new_name = self.anonymizes_name(full_name_list, 50-i)
            for i, x in enumerate(new_name):
                self.ftext = re.sub(f'{x[1]}|{x[1].lower()}|{x[1].upper()}|{x[1].title()}', x[0], self.ftext)


    def anonymizes_geo(self):
        fakerGenerator = Faker()
        fakerGenerator.random.seed(2020)

        #substituir por lista completa de cidades

        #common_geo = ['Viseu', "Guimarães", 'Lisboa', 'Guarda', 'Setúbal', 'Leiria', 'Portalegre', 'Porto', 'Bragança', 'Coimbra', 'Vila Real', 'Aveiro', 'Faro', 'Évora', 'Braga', 'Beja', 'Santarém', 'Castelo Branco', 'Viana do Castelo']

        common_geo = open("geo_locations_pt.txt","r").readlines()
        common_geo = [x.strip() for x in common_geo]

        geo_list = [fakerGenerator.local_latlng(country_code='BR', coords_only=False)[2] for i in range(len(common_geo))]
        for i, x in enumerate(common_geo):
            for m in re.finditer(f'\W{x}', self.ftext):
                p = re.sub(r'([^A-Za-z ]+|^ )', '', m.group(0)) 
                self.ftext = re.sub(f'{p}|{p.lower()}|{p.upper()}|{p.title()}', geo_list[i], self.ftext)

    def anonymizes_hospitals_name(self):
        fakerGenerator = Faker()
        for i, m in enumerate(re.finditer(r'(Hospital)((\sde\s|\s)?([A-Z][\w|a-z]+)*)*', self.ftext, re.UNICODE)):
            fakerGenerator.random.seed(i)
            self.ftext = re.sub(f'{m.group()}|{m.group().lower()}|{m.group().upper()}|{m.group().title()}', 'Hospital ' + fakerGenerator.company(), self.ftext)


    # Write text file anonymized
    def rewrite_txt(self):
        #text_file = open(self.filename, "w")
        #n = text_file.write(self.ftext)
        #text_file.close()

        text_file = codecs.open(self.filename, "w", "utf-8")
        text_file.write(self.ftext)
        text_file.close()

    def anonymizes(self):
        print('\n\n')
        text_file = open(self.filename, "r")
        self.ftext = text_file.read()

        #print('» detect named entities using spacy' + self.filename)        
        #self.detect_named_entities()
        self.load_nomes_communs()

        print("hide age mentions")
        self.hide_age_mentions()

        print('» anonymizing patient\'s name of ' + self.filename)
#        self.anonymizes_patient_name()

        print('» anonymizes doctors name of ' + self.filename)
#        self.anonymizes_dr_names()

        print('» anonymizes other names of ' + self.filename)
#        self.anonymizes_other_names()

        print('» removing headers of ' + self.filename)
        self.remove_headers()

        print('» anonymizing dates of ' + self.filename)
        self.anonymizes_dates()

        print('» anonymizing cities of ' + self.filename)
        self.anonymizes_geo()

        print('» anonymizing hospitals\' names of ' + self.filename)
        self.anonymizes_hospitals_name()

        print('» finish proper names anonymization  ' + self.filename)
        
        self.anonymizes_commmon_names()

        print('» rewriting ' + self.filename)
        self.rewrite_txt()
