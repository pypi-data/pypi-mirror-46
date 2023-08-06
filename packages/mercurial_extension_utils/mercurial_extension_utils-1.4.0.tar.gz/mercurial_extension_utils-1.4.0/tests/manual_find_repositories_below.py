
import mercurial_extension_utils as meu

#for repo_path in meu.find_repositories_below("~/DEV_hg/mercurial"):
for repo_path in meu.find_repositories_below("~/DEV_hg"):
    print repo_path
