require(stringr)
library(tidyr)
procesamiento <- read.csv(file="tweetsIG.csv",header=TRUE,sep="|")

filtro<-subset(procesamiento,str_sub(fecha,start=-4)=="2018")
filtro2<-subset(filtro,grepl("Rev.",contenido))
filtro2$contenido<-str_sub(filtro2$contenido,start=gregexpr("2018(-|/)",filtro2$contenido))
filtro4<-subset(filtro2,str_sub(contenido,start=1,end=5)=="2018/")
filtro4$fecha<-NULL

filtro5<-filtro4 %>%separate(contenido, c("datos1", "datos2","provincia"), ",")
filtro6<-filtro5 %>%separate(datos1, c("fechaHora", "tl","magNumber","prof","profundidad","km"), " ")
filtro7<-filtro6 %>%separate(fechaHora,c("fecha","hora"),"-")
filtro8<-filtro7 %>%separate(magNumber,c("mag","magnitud"),":")
filtro8$provincia<-str_sub(filtro8$provincia,end =gregexpr(" http",filtro8$provincia))
filtro8$tl<-NULL
filtro8$mag<-NULL
filtro8$prof<-NULL
filtro8$km<-NULL
filtro8$datos2<-NULL

write.table(filtro8, "filtrado.csv", append = FALSE, sep = "|",row.names = FALSE, col.names = TRUE,quote = FALSE)