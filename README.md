# EstoyBien - Telegram Chatbot

## Instrucciones

1. Renombrar `config/development.conf.sample` por `config/development.conf` y poner claves

2. Correr

```
python bin/main.py
```

## Sphinx

Para correr sphinx, pararse en la carpeta de sphinx y correr el siguiente comando (o actualizar el path de los parametros -dict y -lm)

```

pocketsphinx_continuous -hmm /home/damifur/Facultad/procesamiento_del_habla/TP2/tp2-prochabla/pocketsphinx/cmusphinx-es-5.2/model_parameters/voxforge_es_sphinx.cd_ptm_4000/ -lm es-20k.lm.gz -dict es.dict -inmic yes

```


## Correr Ejemplos

```
$ python ejemplos/tts.py
```