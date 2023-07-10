--BASES DE DATOS --
-.PARA LAS BASES DE DATOS YO UTILICE POSTGRES:
    LA CREACION DE LAS BASES DE DATOS ESTAN DENTRO DE CREATEDB.PY AHI SE PODRAN ENCONTRAR LOS QUERYS PARA LAS TABLAS QUE UTILICE
        -PRODUCT
        -ADMINUSER

--USO DE LIBRERIAS--
    DENTRO DE REQUIREMENTS.TXT LO SUBI PARA QUE SEVEAN MI ENTORNO, NO TODOS LAS LIBRERIAS ESTAN USADAS AQUI, SON LAS QUE TENGO EN MI ENTORNO PERSONAL
--uso de flask mail:
Less secure apps & your Google Account
To help keep your account secure, from May 30, 2022, ​​Google no longer supports the use of third-party apps or devices which ask you to sign in to your Google Account using only your username and password.

Important: This deadline does not apply to Google Workspace or Google Cloud Identity customers. The enforcement date for these customers will be announced on the Workspace blog at a later date.

For more information, continue to read.
lamentablemente se me imposibilito realizar la prueba con flask tengo un ejemplo de como hacer la llamada en /routes/configure_routes en el endpoint "delete_product"ln: 137 lo dejare comentado para que funcione el end point

--Templates---
tiene todos y cada uno de las plantillas html que se utilizaron para este proyecto

--test--
el archivo test_endpoint tiene algunas pruebas unitarias simuladas
con el objetivo de verificar la funcionalidad del endpoint

--static--
es una carpeta que utilizo para tomar recursos de estilos y de JS

--Model-- se encuentran los modelos de las DB 

-- databases-- se encuentras las conexiones a las bases de datos y el query de las 2 que utilice 

--.ENV-- es es mi entorno con algunas variables

--Routes-- esta carpeta contiene logica de las vistas asi y querys para la utilizacion de la pagina

--Resources--Logica de modelo query/sevidor
--myenv mi ambiente virutal
--a nivel aplicacion tengo 3 archivos:
            -app.py para correr la aplicacion   
            --config para cargar algunas configuraciones
            - requirements.para facilitar la reproduccion de este proyecto