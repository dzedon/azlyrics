Imagina la siguiente situación: el cliente está haciendo una 
aplicación donde necesita desarrolladores para reunir información sobre 
artistas, canciones, albums y letras. 

La fase uno del proyecto es una pequeña araña/scrapper que navegará en 
azlyrics y extraerá la información ya mencionada sobre artistas y sus letras. 
La información adquirida puede ser visualizada mediante simples endpoints de 
navegación, esto es endpoints para mostrar los artistas (paginación y filtros),
albums (paginación y filtros) y canciones (paginación y filtros), 
o bien, directamente todos los albums y canciones. 
Un ejemplo de esto en REST sería:

```
/artist/                   => muestra una lista de todos los artistas
/artist/<artist_id>        => muestra una lista de todos los albums relacionados al artista seleccionado
/artist/<artist_id>/<album_id>            => muestra las canciones pertenecientes al album del artista seleccionado
/artist/<artist_id>/<album_id>/<song_id>  => muestra las canciones pertenecientes al album del artista seleccionado
```
A parte también:
```
/album/   => muestra todos los albums que han sido almacenados por el scrapper
/song/    => muestra una lista de toda las canciones
```
Nota: los endpoints ```/artist/```, /```album/```, ```/song/``` 
deben implementar filtros y paginación. Django tiene clases para manejo nativo de estas características

Tener en cuenta:
- Auth no es necesario por el momento
- Usar solamente canciones en inglés
- Es una API por lo que un front-end no debe ser implementado
- Para facilitar la gestión implementar Django-Admin y los modelos necesarios


Durante la fase dos, los analistas quieren poder hacer el análisis léxico 
de las palabras más y menos usadas, para ello existirá un 
endpoint donde puedas establecer el número de letras mínimo que debe de tener 
la palabra, las apariciones totales mínimas o máximas. 

Ejemplo:

```
Apariciones mínimas: 10
Apariciones máximas: 100
Número mínimo de letras en la palabra: 4



{
    "heart": {
        "songs_number": 12,
        "average": 5,
        "most_used_by": "The heart artist"
    },
    "life": {
        "songs_number": 98,
        "average": 37,
        "most_used_by": "Bon Jovi"
    },
    {
        ...
    },
    ...
}
```
Nota: Es válido hacer uso de alguna librería lexicográfica para detectar 
y separar artículos de sustantivos. 
Como el idioma de las canciones inglés es fácil encontrar librerías que hagan 
esto. Ejemplo nltk o spacy

A partir de esta fase, lo registros ya existentes en la base de datos pueden 
actualizarse y borrarse. 
Para poder llevar a cabo esta administración se deberá implementar la 
autenticación de usuarios, 
teniendo roles como Admin, Analist más el rol Unauthenticated . 

De ser necesario se pueden implementar más roles y permisos.
```
Admin: CRUD de los registros
Analist: Actualizar artistas, albums y canciones
UnAuth: Read
```

Nota: la operación de Delete será un soft delete. Esto quiere decir que los registros en DB no son borrados sino deshabilitados.
Importante: La generación de permisos y grupos deberá de ser hecha mediante migraciones
pr-approved
heart
smile


Si de verdad quieres el desafío completo empieza con nodejs 
pero te aconsejo hacerlo en Python, 
ya que tengas un poco entendido el problema entonces usar nodejs
Igual esto es un dummy project entonces no lo veas como algo que va a ser 
utilizado y que tiene que tener coherencia, sino más bien es con 
finalidad de practicar herramientas de código