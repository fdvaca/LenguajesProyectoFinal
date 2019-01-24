import vizualizacion as vi

sismos=vi.leerarchivo("filtrado.csv")
vi.crearPastelProfundidad(sismos)
vi.crearGraficoBarrasFranja(sismos)
vi.crearGraficoBarrasMagnitud(sismos)
vi.crearGraficaPastel(sismos)

