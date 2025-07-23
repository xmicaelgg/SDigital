import re

def extraer_imeis(texto: str, omitir_pares=False) -> list:
    # Buscar todos los números de 15 dígitos
    imeis = re.findall(r'\b\d{15}\b', texto)
    # Eliminar duplicados manteniendo el orden
    seen = set()
    imeis_unicos = []
    for imei in imeis:
        if imei not in seen:
            seen.add(imei)
            imeis_unicos.append(imei)
    # Si omitir_pares, solo tomar los de posiciones impares (1,3,5...)
    if omitir_pares:
        imeis_unicos = [imei for idx, imei in enumerate(imeis_unicos) if idx % 2 == 0]
    return imeis_unicos 