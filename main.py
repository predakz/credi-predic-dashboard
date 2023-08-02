# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:33:33 2023

@author: Paul
"""

import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px

# Online URL hosting the API
URL = "https://credi-predic-490718cd231c.herokuapp.com/predict"

# Function sending the request to the API and returning the data from the API
def request_prediction(model_url, payload):
    # Sending the request
    response = requests.get(model_url, params=payload)
    # Returning an error if the status is not 200 (= success)
    if response.status_code != 200:
        raise Exception(
            "Echec de la requête, code d'erreur: ", response.status_code, '\n', response.text
        )
    return response

def main():
    # Generating a title
    st.title('Candidature à un prêt')
    # Displaying a bar to enter the ID with maximum and minimum values
    id_number = st.number_input(
                label = 'ID client:',
                min_value = 100002,
                max_value = 456255
        )
    id_number = int(id_number)
    # Checkbox allowing to choose if we want to display the user info
    show_info = st.checkbox(label='Afficher les données client', value=True)
    # Button to submit the ID and generate the prediction
    submitted = st.button('Entrer')
    # Once "submit" button clicked:
    if submitted:
        with st.spinner('Chargement...'):
            # Part of the request containing the parameters (the ID)
            payload = {'customer': str(id_number)}
            # Sending the request and getting data
            response = request_prediction(URL, payload).json()
            # returning the error if there is one
            if response['Statut'] == 'Erreur':
                st.write(response['Message'])
            else:
                # Showing score (probability), threshold and prediction for the client
                st.write('Score (probabilité) :', response['Score'], '/ 1')
                st.write("Seuil d'acceptation :", response['Seuil'])
                st.write('Prédiction :', response['Prédiction'])
                # Displaying a message saying if the credit can be granted or not
                if response['Prédiction'] == 1:
                    st.write('Crédit accordé')
                else:
                    st.write('Crédit refusé')
                # Displaying the explainer
                st.write('Détails:')
                names = []
                colors = []
                for i in response['Explainer list']:
                    names.append(i[0])
                for i in range(len(response['Explainer map']['Feature_idx'])):
                    colors.append('green' if response['Explainer map']['Scaled_value'][i] > 0 else 'red')
                values = [i for i in response['Explainer map']['Scaled_value']]
                names.reverse()
                values.reverse()
                colors.reverse()
                # Generating the bar plot of the explainer
                fig = plt.figure(figsize=(12, 8))
                plt.barh(range(len(names)), values, tick_label=names, color=colors)
                plt.title('Paramètres les plus importants:')
                plt.grid()
                st.pyplot(fig)
                for i in response['Distributions']:
                    fig = px.histogram(response['Distributions'][i], nbins=40, title=i)
                    fig.add_vline(
                        x=response['Infos utilisateur'][i][str(id_number)],
                        annotation_text=str(response['Infos utilisateur'][i][str(id_number)]),
                        annotation_position='top right'                    
                    )
                    st.plotly_chart(fig)
                if show_info:
                    st.write('Données client:')

                    st.json(response['Infos utilisateur'])
        st.success("Merci d'avoir utilisé notre service") 
         
if __name__ == '__main__':
    main()