# Como correr comandos

```
TELEGRAM_TOKEN=<token> python programa.py

```

#Para correr sphinx, pararse en la carpeta de sphinx y correr el siguiente comando (o actualizar el path de los parametros -dict y -lm)

```

pocketsphinx_continuous -hmm /home/damifur/Facultad/procesamiento_del_habla/TP2/tp2-prochabla/pocketsphinx/cmusphinx-es-5.2/model_parameters/voxforge_es_sphinx.cd_ptm_4000/ -lm es-20k.lm.gz -dict es.dict -inmic yes

```


# Ejemplos

```
$ python ejemplos/tts.py
```