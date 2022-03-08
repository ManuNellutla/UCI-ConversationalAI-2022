import sys
import pandas as pd
import json


def main(dict):
    intent = dict["intent"]
    df_movie_abt = pd.read_csv("https://raw.githubusercontent.com/drarvindsathi/movie_recommender_data/main/data/movie_abt_with_rating.csv")
    movie_json_list = json.loads(df_movie_abt.to_json(orient="records"))

        
    if intent == "recommend-movie-by-genre":
        find_keyword = False
        try:
            entity_type_1 = dict["entity_type_1"]
            entity_value_1 = dict["entity_value_1"]
        except:
            entity_type_1 = ""
            entity_value_1 = ""
        try:
            entity_type_2 = dict["entity_type_2"]
            entity_value_2 = dict["entity_value_2"]
        except:
            entity_type_2 = ""
            entity_value_2 = ""    
        if entity_type_1 == "genre":
            genre_to_search = entity_value_1
            if entity_type_2 == "keyword":
                keyword_to_search = entity_value_2
                print("genre_to_search: ", entity_value_1)
                print("keyword_to_search: ", entity_value_2)
                
                movie_in_keyword_genre = []
                movie_in_genre = []
                for movie_json in movie_json_list:
                    if movie_json['movie_genre']:
                        if genre_to_search in movie_json["movie_genre"]:
                            #print("find genre movie")
                            if movie_json['keywords']:
                                if keyword_to_search in [i['name'] for i in json.loads(movie_json['keywords'])]:
                                    #print("find keyword")
                                    find_keyword = True
                                    movie_in_keyword_genre.append(movie_json)
                            else:
                                #print("no keyword in such movie")
                                movie_in_genre.append(movie_json)
                if movie_in_keyword_genre:
                    movie_in_keyword_genre.sort(key=lambda x: x["rating"], reverse=True)
                    return {'message': f"We recommend: {movie_in_keyword_genre[0]['title']}"}
                if movie_in_genre:
                    movie_in_genre.sort(key=lambda x: x["rating"], reverse=True)
                    return {'message': f"We don't find movie having keyword - {keyword_to_search}, but we have other recommend: {movie_in_genre[0]['title']}"}
                else: 
                    return {'message': "I could not find a match for this genre."}
            else:
                return {'message': "you did not specify keyword"}
        else:
            return {'message': "you did not specify genre"}