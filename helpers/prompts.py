import sys
from yachalk import chalk
sys.path.append("..")

import json
import ollama.client as client


def extractConcepts(prompt: str, metadata={}, model="mistral-openorca:latest"):
    SYS_PROMPT = (
        "Votre tâche consiste à extraire les concepts clés et les entités non personnelles de l'extrait du document juridique fourni. "
        "Concentrez-vous sur l'identification des concepts les plus importants et fondamentaux, en les décomposant en composants plus simples si nécessaire. "
        "Catégorisez chaque concept dans l'une des catégories suivantes : "
        "[événement, concept_juridique, lieu, artefact, document_juridique, organisation, condition, divers].\n"
        "Formatez votre sortie sous forme de liste JSON avec la structure suivante :\n"
        "[\n"
        "   {\n"
        '       "entité": "Concept extrait",\n'
        '       "importance": Importance du concept sur une échelle de 1 à 5 (5 étant la plus élevée),\n'
        '       "catégorie": "Type de concept",\n'
        "   },\n"
        "   { ... },\n"
        "]\n"
        "Assurez-vous que les concepts extraits sont pertinents dans le contexte juridique et administratif du document."
    )


    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result


def graphPrompt(input: str, metadata={}, model="mistral-openorca:latest"):
    if model == None:
        model = "mistral-openorca:latest"

    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
    "Vous êtes un constructeur de graphes de connaissances chargé d'extraire des termes et leurs relations d'un document juridique. "
    "Un extrait de contexte (délimité par ```) vous est fourni. Votre tâche consiste à extraire l'ontologie des termes "
    "et les relations entre eux décrites dans le contexte.\n\n"
    "Réflexion 1 : En traitant chaque phrase, identifiez les termes ou entités clés mentionnés.\n"
    "   - Les termes peuvent inclure des concepts juridiques, des lieux, des organisations, des individus (références non personnelles), "
    "     des conditions, des acronymes, des documents juridiques, des services, des concepts, etc.\n"
    "   - Assurez-vous que les termes soient aussi spécifiques et atomiques que possible.\n\n"
    "Réflexion 2 : Identifiez les relations entre ces termes.\n"
    "   - Les termes mentionnés dans la même phrase ou paragraphe partagent souvent une relation.\n"
    "   - Un terme peut être lié à plusieurs autres termes.\n"
    "   - Utilisez le contexte juridique pour déduire et décrire la nature de ces relations.\n\n"
    "Réflexion 3 : Définissez clairement la relation entre chaque paire de termes liés.\n"
    "   - Dans la description de la relation ('edge'), ne répétez pas les noms exacts des 'nodes'. "
    "     Décrivez simplement la nature de la relation entre 'node_1' et 'node_2'.\n"
    "   - Veillez à ce que les relations soient concises, précises et pertinentes dans le contexte juridique.\n\n"
    "Formatez votre sortie sous forme de liste d'objets JSON. Chaque objet représente une paire de termes liés et leur relation. "
    "Le format est le suivant :\n"
    "[\n"
    "   {\n"
    '       "node_1": "Un concept ou terme extrait du document juridique",\n'
    '       "node_2": "Un concept ou terme lié extrait du document juridique",\n'
    '       "edge": "Une description concise de la relation entre node_1 et node_2 sans répéter les termes des nœuds"\n'
    "   },\n"
    "   { ... }\n"
    "]\n\n"
        "Veuillez fournir la sortie en français."
)



    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result
