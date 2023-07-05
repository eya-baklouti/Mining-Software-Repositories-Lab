import pandas as pd
HACK_PATTERNS = """hack
retarded
at a loss
stupid
remove this code
ugly
take care
something's gone wrong
nuke
is problematic
may cause problem
hacky
unknown why we ever experience this
treat this as a soft error
silly
workaround for bug
kludge
fixme
this isn't quite right
trial and error
give up
this is wrong
hang our heads in shame
temporary solution
causes issue
something bad is going on
cause for issue
this doesn't look right
is this next line safe
this indicates a more fundamental problem
temporary crutch
this can be a mess
this isn't very solid
this is temporary and will go away
is this line really safe
there is a problem
some fatal error
something serious is wrong
don't use this
get rid of this
doubt that this would work
this is bs
give up and go away
risk of this blowing up
just abandon it
prolly a bug
probably a bug
hope everything will work
toss it
barf
something bad happened
fix this crap
yuck
certainly buggy
remove me before production
you can be unhappy now
this is uncool
bail out
it doesn't work yet
crap
inconsistency
abandon all hope
method name
rename
Tidy up
typo
spelling"""

satd_key_words_list = HACK_PATTERNS.split('\n')

df = pd.read_excel('./final_jessie.xlsx',index_col=None)
is_satd_values = []
has_satd=False
for  index, row in df.iterrows():

    # loop over the list of strings and check if each lowercase substring is in my_string_lower
    for substring in satd_key_words_list:
        if substring.lower() in row['commit_message'].lower():
            print(f"'{substring}' is a substring of '{row['commit_message']}'")
            has_satd = (True)
            continue
    if has_satd:
        is_satd_values.append(True)
    else:
        is_satd_values.append(False)



    


df['is_message_satd'] = is_satd_values

df.to_excel('final_jessie_q2.xlsx', index=False)

print(df)