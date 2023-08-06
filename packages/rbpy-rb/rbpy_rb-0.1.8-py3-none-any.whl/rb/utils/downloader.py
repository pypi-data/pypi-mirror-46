import json
from rb.utils.rblogger import Logger
import os
import sys
import zipfile

import wget

from rb.core.lang import Lang

LINKS = {
    Lang.EN: {
        'models': {
            'coca': "https://nextcloud.readerbench.com/index.php/s/H5ccMZwRLyMffG4/download"
        },
        'spacy': {}

    },
    Lang.RO: {
        'models': {
            'diacritics': "https://nextcloud.readerbench.com/index.php/s/pfC25G64JgxcfZS/download",
            'readme': "https://nextcloud.readerbench.com/index.php/s/g9etLBeSTmKxjM8/download",
        },
        'spacy': {
            'ro_ud_ft_ner': "https://nextcloud.readerbench.com/index.php/s/GLdDH8R4jpkFfnd/download",
        },
        'wordnet': "https://nextcloud.readerbench.com/index.php/s/7tDka2CSGYeJqgC/download"
    },
    Lang.RU: {
        'spacy': {
            'ru_ud_ft': "https://nextcloud.readerbench.com/index.php/s/nbErkdgbxmgiRCG/download"
        }
    }
}

logger = Logger.get_logger()

def download_folder(link: str, destination: str):
    os.makedirs(destination, exist_ok=True)     
    filename = wget.download(link, out=destination, bar=wget.bar_thermometer)
    logger.info('Downloaded {}'.format(filename))
    if zipfile.is_zipfile(filename):
        logger.info('Extracting files from {}'.format(filename))
        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(destination)
        os.remove(filename)
    

def download_model(lang: Lang, name: str) -> bool:
    if not lang in LINKS:
        logger.info('{} not supported.'.format(lang))
        return False
    if not name in LINKS[lang]['models']:
        logger.info('No model named {}.'.format(name))
        return False
    logger.info("Downloading model {} for {} ...".format(name, lang.value))
    link = LINKS[lang]['models'][name]
    folder = "resources/{}/models/".format(lang.value)
    download_folder(link, folder)
    return True

def download_spacy_model(lang: Lang, name: str = 'latest') -> bool:
    if not lang in LINKS:
        return False
    if not name in LINKS[lang]['spacy']:
        return False
    logger.info("Downloading spacy model {} for {}...".format(name, lang.value))
    link = LINKS[lang]['spacy'][name]
    folder = "resources/{}/spacy/".format(lang.value)
    download_folder(link, folder)
    return True

def download_wordnet(lang: Lang, folder: str) -> bool:
    if lang not in LINKS:
        logger.info('{} not supported.'.format(lang))
        return False
    if 'wordnet' not in LINKS[lang]:
        logger.info('No WordNet found')
        return False
    link = LINKS[lang]['wordnet']
    download_folder(link, folder)
        
if __name__ == "__main__":
    download_model(Lang.EN, 'coca')
