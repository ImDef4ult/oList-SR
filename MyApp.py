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
        olist es una empresa de tecnología del tipo SaaS (Software as a Service) fundada en 2015 
        que ofrece una solución para el aumento de las ventas de comerciantes de todos los tamaños, 
        para la mayoría de los segmentos, que tengan presencia en línea o no.

        La solución de olist se compone de tres frentes: Software, contratos con los principales 
        mercados y compartición de reputación. Estos tres frentes juntos forman el servicio inédito 
        de olist, sin comparación con cualquier otro servicio existente en el mundo.

        El cliente olist cuenta con las ventajas específicas de cada uno de los frentes, 
        como por ejemplo:

            – Software: Gestión de pedidos centralizados (pedidos de cualquiera de los diversos 
            marketplaces administrados en una sola plataforma), datos para envío, generación de 
            etiquetas personalizadas, entre otros servicios.

            – Contratos exclusivos: olist cuenta con contratos ya firmados con los principales 
            marketplaces de Brasil, además de un contrato extremadamente ventajoso con los Correos. 
            Por medio de olist – y de sólo un contrato – comerciantes pueden comenzar a vender en 
            varios marketplaces, acortando caminos para el aumento de las ventas. No es necesario 
            tener contratos directos con los marketplaces. Tú utilizas nuestro contrato y listo!

            – Compartición de reputación: Como olist es también una gran tienda de departamentos, 
            todas las ventas realizadas en olist dentro de los marketplaces generan altísima 
            reputación que es compartida entre todos los comerciantes participantes. Incluso los 
            comerciantes recién iniciados en el mundo de las ventas pueden beneficiarse de espacios 
            privilegiados, campañas y otras facilidades que sólo un servicio como el de olist puede 
            ofrecer.
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
    
    imageTransit  = Image.open('Data/Banner_2.jpg')
    st.image(imageTransit, use_column_width=True)

    st.header('Recomendaciones para ti!')
    user_cat = mt.get_user_behavior(userName)
    if (user_cat == 'moveis_decoracao') | (user_cat == 'construcao_ferramentas_construcao'):
        pass
    else:
        user_cat = 'oList'

    Tmp_Reco = mt.getSVDReco(userName)

    Reco_1_Image, Reco_1_detail = st.beta_columns(2)
    with Reco_1_Image:
        Rec_1  = Image.open(f'Data/{user_cat}_1.jpg')
        st.image(Rec_1, use_column_width=True)
    with Reco_1_detail:
        Reco1_name = Tmp_Reco.iloc[0]['product_id']
        st.subheader(f'1. {Reco1_name}')
        Reco1_detail = mt.getProductDetail(Reco1_name)

        Reco_1_Cat = Reco1_detail['product_category_name'].values[0]
        st.write(f'**Categoria: ** {Reco_1_Cat}')
        st.write()

        Reco_1_Weight = Reco1_detail['product_weight_g'].values[0]
        st.write(f'**Peso (gr): ** {Reco_1_Weight}')

        st.write('**Medidas (cm)**')
        Reco_1_Height = Reco1_detail['product_height_cm'].values[0]
        st.write(f'Alto: {Reco_1_Height}')

        Reco_1_width = Reco1_detail['product_width_cm'].values[0]
        st.write(f'Alto: {Reco_1_width}')

        Reco_1_length = Reco1_detail['product_length_cm'].values[0]
        st.write(f'Alto: {Reco_1_length}')


    Reco_2_detail, Reco_2_Image = st.beta_columns(2)
    with Reco_2_detail:
        Reco2_name = Tmp_Reco.iloc[1]['product_id']
        st.subheader(f'2. {Reco2_name}')
        Reco2_detail = mt.getProductDetail(Reco2_name)

        Reco_2_Cat = Reco2_detail['product_category_name'].values[0]
        st.write(f'**Categoria: ** {Reco_2_Cat}')
        st.write()

        Reco_2_Weight = Reco2_detail['product_weight_g'].values[0]
        st.write(f'**Peso (gr): ** {Reco_2_Weight}')

        st.write('**Medidas (cm)**')
        Reco_2_Height = Reco2_detail['product_height_cm'].values[0]
        st.write(f'Alto: {Reco_2_Height}')

        Reco_2_width = Reco2_detail['product_width_cm'].values[0]
        st.write(f'Alto: {Reco_2_width}')

        Reco_2_length = Reco2_detail['product_length_cm'].values[0]
        st.write(f'Alto: {Reco_2_length}')
    with Reco_2_Image:
        Rec_2  = Image.open(f'Data/{user_cat}_2.jpg')
        st.image(Rec_2, use_column_width=True)


    Reco_3_Image, Reco_3_detail = st.beta_columns(2)
    with Reco_3_Image:
        Rec_3  = Image.open(f'Data/{user_cat}_3.jpg')
        st.image(Rec_3, use_column_width=True)
    with Reco_3_detail:
        Reco3_name = Tmp_Reco.iloc[2]['product_id']
        st.subheader(f'3. {Reco3_name}')
        Reco3_detail = mt.getProductDetail(Reco3_name)

        Reco_3_Cat = Reco3_detail['product_category_name'].values[0]
        st.write(f'**Categoria: ** {Reco_3_Cat}')
        st.write()

        Reco_3_Weight = Reco3_detail['product_weight_g'].values[0]
        st.write(f'**Peso (gr): ** {Reco_3_Weight}')

        st.write('**Medidas (cm)**')
        Reco_3_Height = Reco3_detail['product_height_cm'].values[0]
        st.write(f'Alto: {Reco_3_Height}')

        Reco_3_width = Reco3_detail['product_width_cm'].values[0]
        st.write(f'Alto: {Reco_3_width}')

        Reco_3_length = Reco3_detail['product_length_cm'].values[0]
        st.write(f'Alto: {Reco_3_length}')


    Reco_4_detail, Reco_4_Image = st.beta_columns(2)
    with Reco_4_detail:
        Reco4_name = Tmp_Reco.iloc[3]['product_id']
        st.subheader(f'4. {Reco4_name}')
        Reco4_detail = mt.getProductDetail(Reco4_name)

        Reco_4_Cat = Reco4_detail['product_category_name'].values[0]
        st.write(f'**Categoria: ** {Reco_4_Cat}')
        st.write()

        Reco_4_Weight = Reco4_detail['product_weight_g'].values[0]
        st.write(f'**Peso (gr): ** {Reco_4_Weight}')

        st.write('**Medidas (cm)**')
        Reco_4_Height = Reco4_detail['product_height_cm'].values[0]
        st.write(f'Alto: {Reco_4_Height}')

        Reco_4_width = Reco4_detail['product_width_cm'].values[0]
        st.write(f'Alto: {Reco_4_width}')

        Reco_4_length = Reco4_detail['product_length_cm'].values[0]
        st.write(f'Alto: {Reco_4_length}')
    with Reco_4_Image:
        Rec_4  = Image.open(f'Data/{user_cat}_4.jpg')
        st.image(Rec_4, use_column_width=True)


    Reco_5_Image, Reco_5_detail = st.beta_columns(2)
    with Reco_5_Image:
        Rec_5  = Image.open(f'Data/{user_cat}_5.jpg')
        st.image(Rec_5, use_column_width=True)
    with Reco_5_detail:
        Reco5_name = Tmp_Reco.iloc[4]['product_id']
        st.subheader(f'5. {Reco5_name}')
        Reco5_detail = mt.getProductDetail(Reco5_name)

        Reco_5_Cat = Reco5_detail['product_category_name'].values[0]
        st.write(f'**Categoria: ** {Reco_5_Cat}')
        st.write()

        Reco_5_Weight = Reco5_detail['product_weight_g'].values[0]
        st.write(f'**Peso (gr): ** {Reco_5_Weight}')

        st.write('**Medidas (cm)**')
        Reco_5_Height = Reco5_detail['product_height_cm'].values[0]
        st.write(f'Alto: {Reco_5_Height}')

        Reco_5_width = Reco5_detail['product_width_cm'].values[0]
        st.write(f'Alto: {Reco_5_width}')

        Reco_5_length = Reco4_detail['product_length_cm'].values[0]
        st.write(f'Alto: {Reco_5_length}')