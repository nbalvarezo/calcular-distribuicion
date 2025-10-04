

#Pago_Principal=Monto_Total−∑(Pagos_Adicionales)

# Septiembre 30, 2025
# Mdidor principal: 64409
# Medidor 1: 10083
# Medidor 2: 1275
# Medidor 3: 9919
# Medidor 4: 9182
# Total cuenta: $516100

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

def calcular_distribucion(consumo_principal, consumos_adicionales, monto_total):
    total_adicionales_kWh = sum(consumos_adicionales)
    total_general = consumo_principal
    # total_general = consumo_principal + total_adicionales_kWh

    resultados = []

    # Medidores adicionales
    for i, consumo in enumerate(consumos_adicionales, start=1):Mdidor p        porcentaje = (consumo / total_general * 100) if total_general > 0 else 0
        pago = (consumo / total_general * monto_total) if total_general > 0 else 0
        resultados.append({
            "Medidor": f"Adicional {i}",
            "Consumo (kWh)": consumo,
            "% del total general": porcentaje,
            "Monto a pagar ($)": pago
        })

    # Medidor principal
    porcentaje_principal = (consumo_principal / total_general * 100) if total_general > 0 else 0
    pago_principal = (consumo_principal / total_general * monto_total) if total_general > 0 else 0

    resultados.append({
        "Medidor": "Principal",
        "Consumo (kWh)": consumo_principal,
        "% del total general": porcentaje_principal,
        "Monto a pagar ($)": pago_principal
    })

    return resultados, total_adicionales_kWh, total_general, monto_total

def mostrar_en_consola(resultados, total_adicionales, total_general, monto_total):
    print("\n--- Resumen de pagos ---")
    for r in resultados:
        print(f"{r['Medidor']}: {r['Consumo (kWh)']:.2f} kWh | "
              f"{r['% del total general']:.2f}% del total | "
              f"Paga: ${r['Monto a pagar ($)']:.2f}")

    print(f"\nTotal adicionales: {total_adicionales:.2f} kWh")
    print(f"Total general: {total_general:.2f} kWh")
    print(f"Monto total de la cuenta: ${monto_total:.2f}")

def exportar_excel(resultados, total_adicionales, total_general, monto_total, filename="reporte_consumo.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Distribución Consumo"

    headers = ["Medidor", "Consumo (kWh)", "% del total general", "Monto a pagar ($)"]
    ws.append(headers)

    for col in ws[1]:
        col.font = Font(bold=True)
        col.alignment = Alignment(horizontal="center")

    for r in resultados:
        ws.append([
            r["Medidor"],
            round(r["Consumo (kWh)"], 2),
            f"{r['% del total general']:.2f}%",
            round(r["Monto a pagar ($)"], 2)
        ])

    ws.append([])
    ws.append(["TOTAL adicionales", total_adicionales, "-", "-"])
    #ws.append(["TOTAL general", total_general, "100%", round(monto_total, 2)])

    wb.save(filename)
    print(f"\n✅ Reporte guardado en: {filename}")

def main():
    consumo_principal = float(input("Ingrese el consumo del medidor principal (kWh): ").strip())
    n = int(input("Ingrese la cantidad de medidores adicionales: ").strip())
    consumos_adicionales = []
    for i in range(n):
        valor = float(input(f"Ingrese el consumo del medidor adicional {i+1} (kWh): ").strip())
        consumos_adicionales.append(valor)

    monto_total = float(input("Ingrese el monto total de la cuenta ($): ").strip())

    resultados, total_adicionales, total_general, monto_total = calcular_distribucion(
        consumo_principal, consumos_adicionales, monto_total
    )

    mostrar_en_consola(resultados, total_adicionales, total_general, monto_total)
    exportar_excel(resultados, total_adicionales, total_general, monto_total)

if __name__ == "__main__":
    main()
