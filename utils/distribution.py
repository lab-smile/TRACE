"""
This module contains a dictionary that maps ancestry categories to lists of related terms.
It is used for checking the correctness of ancestry information retrieved from various sources.
"""

distribution = {
    "African": [
        "African", "Sub-Saharan African", "West African", "East African", 
        "North African", "Central African", "Southern African", "Black", 
        "African American", "Afro-Caribbean", "African descent", 
        "African-derived", "African origin", "African ancestry", 
        "African ethnicity", "African lineage", "African heritage", 
        "African population", "African cohort", "African sample", 
        "African genetic background", "African genomic profile"
    ],
    "Native American": [
        "Native American", "Indigenous American", "American Indian", 
        "First Nations", "Aboriginal American", "Amerindian", 
        "Indigenous peoples of the Americas", "Native ancestry", 
        "Native American descent", "Native American origin", 
        "Indigenous American lineage", "American Indian heritage", 
        "Native American population", "Indigenous American cohort", 
        "Native American sample", "Amerindian genetic background", 
        "Indigenous American genomic profile"
    ],
    "East Asian, North": [
        "East Asian", "Northeast Asian", "Northern East Asian", 
        "Chinese", "Japanese", "Korean", "Mongolian", "Siberian", 
        "East Asian ancestry", "East Asian descent", "East Asian origin", 
        "Northeast Asian lineage", "Northern East Asian heritage", 
        "East Asian population", "Northeast Asian cohort", 
        "Northern East Asian sample", "East Asian genetic background", 
        "Northeast Asian genomic profile"
    ],
    "East Asian, South": [
        "Southeast Asian", "Southern East Asian", "Pacific Islander", 
        "Austronesian", "Southeast Asian ancestry", "Southern East Asian descent", 
        "Pacific Islander origin", "Austronesian lineage", 
        "Southeast Asian heritage", "Southern East Asian population", 
        "Pacific Islander cohort", "Austronesian sample", 
        "Southeast Asian genetic background", "Southern East Asian genomic profile"
    ],
    "South Asian": [
        "South Asian", "Indian subcontinent", "Indo-Aryan", "Dravidian", 
        "South Asian ancestry", "Indian subcontinent descent", 
        "Indo-Aryan origin", "Dravidian lineage", "South Asian heritage", 
        "Indian subcontinent population", "South Asian cohort", 
        "Indo-Aryan sample", "Dravidian genetic background", 
        "South Asian genomic profile"
    ],
    "European, North": [
        "European", "Northern European", "Northwestern European", "Nordic", "Germanic", 
        "Anglo-Saxon", "Celtic", "Scandinavian", "Baltic", 
        "Northern European ancestry", "Northwestern European descent", 
        "Nordic origin", "Germanic lineage", "Anglo-Saxon heritage", 
        "Celtic population", "Scandinavian cohort", "Baltic sample", 
        "Northern European genetic background", "Northwestern European genomic profile"
    ],
    "European, South": [
        "European", "Southern European", "Mediterranean", "Balkan", "Iberian", 
        "Italian", "Greek", "Slavic", "Southern European ancestry", 
        "Mediterranean descent", "Balkan origin", "Iberian lineage", 
        "Italian heritage", "Greek population", "Slavic cohort", 
        "Southern European sample", "Mediterranean genetic background", 
        "Balkan genomic profile"
    ]
}