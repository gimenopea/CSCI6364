from congress import Congress
import pandas as pd

congress_api = Congress('iJLW19g0StJ1Q0RA0dRH9YUzrtzZDFmEfoaaJZAK')

#get congressional member history and output to members.csv
def get_members():
    result = []
    for i in range(107,118):
        year_elected = 2021 - (2 * (117 - i))

        members = []
        for c in congress_api.members.filter('senate', i)[0]['members']:
            members.append([c['id'],c['first_name'] ,c['middle_name'],c['last_name'] , c['state'] , i,year_elected] )

        result.extend( members )

    pd.DataFrame(result).to_csv('members.csv', header=False, index=False)

#updated congressional member history with open secrets CID and ouput to members_cid.csv
def add_member_cid():


    result = pd.read_csv('members.csv')
    cid_column = [''] * len(result.values)

    buffs={}
    for i in range(10, 19, 2):
        buffs[f"20{i}"] = pd.read_csv(f"candidates/cands{i}.txt", quotechar="|")

    n =0
    for i in range(len(result)):

        _, first_name, _, last_name, state, _, year_elected = result.values[i]

        if year_elected not in range(2011, 2020, 2):
            continue

        canidate_year = f"{year_elected-1}"
        found = None
        for _,_,cid,cname,_,cst,_,_,_,_,_,_ in buffs[canidate_year].values:

            if  last_name in cname and state == cst[:-2]:
                found = cid

        if found == None:
            print(f" NOT FOUND: {first_name} {last_name} in {year_elected}")
            n+=1

        cid_column[i] = found

    result['cid']=cid_column

    pd.DataFrame(result).to_csv('members_cid.csv', header=['ProPublicaID', 'First', 'Middle', 'Last', 'State', 'CD', 'Year', 'CID'], index=False)
    print(f"Done {n} not found")


def main():
    #get_members()
    add_member_cid()

if __name__ == "__main__":
    main()


