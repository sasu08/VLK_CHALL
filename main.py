#!/usr/bin/env python3
import requests
import sys


def progress(i, total):
    """Imprime el progreso de la ejecucion.
    
    Keyword arguments:
    i -- numero del articulo actual.
    total -- cantidad total de articulos.
    """
    
    sys.stdout.write(f"\r{i}/{colored('red',total)}")
    sys.stdout.flush()


def colored(color, text):
    """Colorea el texto en consola.
    
    Keyword arguments:
    color -- color del texto.
    text -- texto a colorear.

    """
    if color == 'red':
        return "\033[38;2;255;0;0m{} \033[38;2;255;255;255m".format(text)
    elif color == 'green':
        return "\033[38;2;0;255;0m{} \033[38;2;255;255;255m".format(text)


def main():
    # Definicion de variables
    offset = 0
    i = 0
    
    try:
        # Lee los argumentos de la linea de comandos.
        SITE = str(sys.argv[1:][0])
        SELLER_ID = str(sys.argv[2:][0])
        # Define las URL de la API.
        URL = f'https://api.mercadolibre.com/sites/{SITE}/search?'
        URL_CAT = 'https://api.mercadolibre.com/categories/'
        
        # Almacena en una variable el resultado de la peticion.
        res = requests.get(URL, params={
                                        'seller_id': SELLER_ID
                                    })
        # Almacena el contenido de la respuesta como contenido json. 
        r = res.json()
        # Almacena la cantidad total de articulos.
        cant_articulos = r['paging']['total']
        # Almacena la cantidad de articulos por pagina.
        limit = r['paging']['limit']
        
        # Condicional que verifica si existen articulos.
        if cant_articulos == 0:
            print("No hay articulos")
            sys.exit()
            
        # Si la peticion fue exitosa, imprime el resultado.
        elif res.status_code == 200:
            with open('lista.log','w') as log_file:
                while(offset < cant_articulos):
                    # Obtiene la lista de items. Cambia con cada iteracion.
                    articulos = requests.get(URL, params={
                                                            'seller_id': SELLER_ID, 
                                                            'offset': offset
                                                        })
                    # Redefinicion de la variable. 
                    articulos = articulos.json().get('results')
                    # Recorre la lista de items e imprime los datos solicitados.
                    for articulo in articulos:
                        # Concatena la URL de la categoria.
                        res_cat = requests.get(URL_CAT + articulo.get('category_id'))
                        # Obtiene datos de la categoria. Es necesario crear esta variable para acceder a los datos de la categoria.
                        r_cat = res_cat.json()
                        log_file.write(f"------------------\
                                                    \n- ITEM ID: {articulo.get('id')}\
                                                    \n- TITULO: {articulo.get('title')}\
                                                    \n- ID DE LA CATEGORIA: {articulo.get('category_id')}\
                                                    \n- NOMBRE DE LA CATEGORIA: {r_cat.get('name')}\
                                                    \n")
                        i+=1
                        progress(i, cant_articulos)
                        
                    # Acumula el offset para la siguiente iteracion.
                    offset+=limit              
                            
                log_file.write(('------------------\n\nCantidad de articulos: ' + str(i)))
                print(f"\n{colored('green', 'Lista de articulos generada con exito.')}")
                
        else:
            # Si la peticion no fue exitosa, imprime el codigo de error.
            print(colored('red','Error: '+str(res.status_code)))
            print({res.raise_for_status()})
    
    
    # Si ocurre un error en la cantidad de parametros ingresados desde consola, imprime el error.
    except IndexError:
        raise Exception(colored('red','ingrese nombre de sitio e ID de vendedor.\
        \n  - Ejemplo: python3 main.py MLA 179571326'))
    
    
    # Si ocure un error en la posicion de los parametros desde consola, imprime el error.
    except KeyError:
        raise Exception(colored('red','revise el orden de los parametros.\
        \n  - Ejemplo: python3 main.py MLA 179571326'))
        
        
# Ejecuta el programa.
if __name__ == '__main__':
    main()
else:
    print('No se puede ejecutar como modulo.')