##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: txt_transformer.py
# Capitulo: Flujo de Datos
# Autor(es): Jose Miguel, Erik, Oscar, Marlon, Carlos
# Version: 2.0.0 Mayo 2024
# Descripción:
#
#   Este archivo define un procesador de datos que se encarga de transformar
#   y formatear el contenido de un archivo HTM
#-------------------------------------------------------------------------

from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, json

class TXTTransformer(luigi.Task):
    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                data_set = txt_file.readlines()
                data = data_set[1:]
                for d in data:
                    lines = d.strip().split(';')
                    for line in lines:
                        fields = line.strip().split(',')
                        if len(fields) >= 8:
                            entry = {
                                "description": fields[2],
                                "quantity": fields[3],
                                "price": fields[5],
                                "total": float(fields[3]) * float(fields[5]),
                                "invoice": fields[0],
                                "provider": fields[6],
                                "country": fields[7]
                            }
                            result.append(entry)
                    
        with self.output().open('w') as out:
            out.write(json.dumps(result, indent =4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))