mkdir -p assets
cd assets

mkdir -p spacy
cd spacy

wget -c https://github.com/explosion/spacy-models/releases/download/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm-3.2.0.tar.gz -O - | tar xz
