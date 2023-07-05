import export_pr
import globals


def ask_user_repo():
    #apache/commons-math test repo
    #TODO Should be changed to cmd
    repo = input("Please enter the repository name (eg owner/reponame): ")
    return repo

def ask_user_export_name():
    #TODO Should be changed to cmd
    export_name = input("What is the export File name? ")
    return export_name

def run_app():
    globals.initialize() 
    print('val is '+str(globals.calls_left))

    print('App is running')
    
    user_input_repo = ask_user_repo()
    export_name = ask_user_export_name()
    
    export_pr.export_features(user_input_repo,export_name)

#Call to start the app to run    
run_app()
