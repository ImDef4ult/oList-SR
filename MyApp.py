import streamlit as st
from Class import method as mt
import ptvsd
import SessionState
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


session_state = SessionState.get(Session=False)
st.set_page_config(layout='wide', page_title='oList SR')

#--------------------------------
# Side Bar
#--------------------------------
Side = st.sidebar
Side.header('Autenticación de usuario')

Side.subheader('Inicio de sesión')
userName = Side.text_input('Usuario')
passUser = Side.text_input('Contraseña', type='password')
LogIn, LogOut = Side.beta_columns(2)

if LogIn.button('LogIn'):
    if len(userName) > 0 and len(passUser) > 0:
            sucess = mt.LogIn(userName, passUser)
            if sucess:
                Side.success('Datos Correctos!')
                session_state.Session = True
            else:
                Side.error('Datos incorrectos...')
    else:
        Side.warning('Ambos campos deben estar completos!')
    
# Banner
imageHome  = Image.open('Data/Banner.png')
st.image(imageHome, use_column_width=True)
st.title('oList Recommendation System')

if session_state.Session is False:
    #About
    About = st.beta_expander("Acerca de")
    About.markdown("""
    * **Autores:** Deyvi Javier Caicedo, Diego Alexander Salgado, 
    German Andres Rojas, Luisa Fernanda Martinez, Nelson Uriel Caicedo,
    Sergio Enrique Alba, Andrés Felipe Rojas
    * **Materia:** Business Analytics
    * **Python libraries:** pandas, streamlit, PIL, Surprise
    * **Data source:** [oList Data set](https://www.kaggle.com/olistbr/brazilian-ecommerce).
    """)

    # Explicacion de la fuente de datos
    oListImage, oListExplain = st.beta_columns((1, 2))
    with oListImage:
        YelpLogo  = Image.open('Data/oList-Logo.png')
        st.image(YelpLogo, use_column_width=True)
    with oListExplain:
        st.write('''
        Yelp es una herramienta que nace con el fin de facilitarle la vida a las personas poniendo a su disposición una 
        plataforma con la que encontrar los mejores negocios de su barrio o de su ciudad. De esta forma, Yelp también 
        apoya el comercio de local y de proximidad.
        
        Dentro de las fuentes de datos, se pueden encontrar varios archivos .json con informacion acerca de:
        - Detalles de los locales (Localizacion, categoria, horarios, etc)
        - Usuarios
        - Reviews de los usuarios hacia los locales con su respectivo puntaje
        - Recomendaciones realizadas por usuarios especificos acerca de un local
        ''')

if session_state.Session is True:
    if LogOut.button('LogOut'):
        session_state.Session = False
        st.experimental_rerun()

    st.header('Tu historial de reviews')
    Summary_Rev, Product_Detail = st.beta_columns(2)
    with Summary_Rev:
        user_Rev = mt.get_UserRev(userName)
        gb = GridOptionsBuilder.from_dataframe(user_Rev)
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value == 'A') {
                return {
                    'color': 'white',
                    'backgroundColor': 'darkred'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            }
        };
        """)
        gb.configure_selection('single', use_checkbox=False)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        grid_response = AgGrid(
            user_Rev, 
            gridOptions=gridOptions,
            height=280, 
            width='100%',
            data_return_mode=DataReturnMode.FILTERED, 
            update_mode=GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=False,
            )
        grid_Selected = grid_response['selected_rows']
    with Product_Detail:
        if grid_Selected:
            Item = grid_Selected[0]
            Selected_item = Item.get('product_id')

            detail, cat = mt.get_ProductDetail(userName, Selected_item)
            st.subheader(f'Detalles del producto: {Selected_item}')
            st.write(f'**Categoria del producto**: {cat}')
            purchase_date = detail['order_purchase_timestamp'].values[0]
            st.write(f'**Fecha de compra**: {purchase_date}')
            price = detail['price'].values[0]
            st.write(f'**Precio**: {price}')
            freight_value = detail['freight_value'].values[0]
            st.write(f'**Valor de envio**: {freight_value}')
    
    st.header('Recomendaciones para ti!')
    user_cat = mt.get_user_behavior(userName)
    st.write(f'Categoria predominante: {user_cat}')

    Reco_1_Image, Reco_1_detail = st.beta_columns(2)
    with Reco_1_Image:
        Rec_1  = Image.open(f'Data/{user_cat}_1.jpg')
        st.image(Rec_1, use_column_width=True)
    with Reco_1_detail:
        pass

    Reco_2_detail, Reco_2_Image = st.beta_columns(2)
    with Reco_2_detail:
        pass
    with Reco_2_Image:
        Rec_2  = Image.open(f'Data/{user_cat}_2.jpg')
        st.image(Rec_2, use_column_width=True)

    Reco_3_Image, Reco_3_detail = st.beta_columns(2)
    with Reco_3_Image:
        Rec_3  = Image.open(f'Data/{user_cat}_3.jpg')
        st.image(Rec_3, use_column_width=True)
    with Reco_3_detail:
        pass

    Reco_4_detail, Reco_4_Image = st.beta_columns(2)
    with Reco_4_detail:
        pass
    with Reco_4_Image:
        Rec_4  = Image.open(f'Data/{user_cat}_4.jpg')
        st.image(Rec_4, use_column_width=True)

    Reco_5_Image, Reco_5_detail = st.beta_columns(2)
    with Reco_5_Image:
        Rec_5  = Image.open(f'Data/{user_cat}_5.jpg')
        st.image(Rec_5, use_column_width=True)
    with Reco_5_detail:
        pass