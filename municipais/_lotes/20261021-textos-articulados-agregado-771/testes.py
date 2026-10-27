import sys,unittest
sys.path.insert(0,'scripts');sys.path.insert(0,'/tmp/constituicao-markdown-qa-20261020')
names=['test_textos_articulados_sapl','test_gates_textos_articulados_sapl','test_contexto_completo_ta','test_emissores_sapl','test_commonmark_ta','test_commonmark_ta_v2','test_data_captura_ta','test_colisoes_lote_municipal']
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in names)
result=unittest.TextTestRunner(verbosity=1).run(suite)
raise SystemExit(not result.wasSuccessful())
