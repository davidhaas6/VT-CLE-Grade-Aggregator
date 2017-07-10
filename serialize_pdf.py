import pickle
from tabula import read_pdf

path = 'cle.pdf'
df = read_pdf(input_path=path, pages='15-25')

f = open('area_2_cles.p', 'w')
pickle.dump(df, f)
f.close()

# convert_into(input_path=path, output_path='test.json', output_format='json', pages='16-24')
print df.info()

for i in range(len(df['COURSE_TITLE'])):
    print str(i) + '\t\t' + str(df['COURSE_TITLE'][i])