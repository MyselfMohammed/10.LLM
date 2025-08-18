# ---------------------- Estimation Retrieval ----------------------
def get_estimation_from_mysql(house_size, vehicle, floor_from, floor_to, distance):
    import mysql.connector     # To connect and interact with MySQL databases
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT charges FROM packing_charges WHERE house_size = %s", (house_size,))
        packing = cursor.fetchone()
        packing_cost = packing['charges'] if packing else 0

        cursor.execute("SELECT loading FROM loading_unloading_charges WHERE house_size = %s AND floor = %s", (house_size, floor_from))
        load = cursor.fetchone()
        load_cost = load['loading'] if load else 0

        cursor.execute("SELECT unloading FROM loading_unloading_charges WHERE house_size = %s AND floor = %s", (house_size, floor_to))
        unload = cursor.fetchone()
        unload_cost = unload['unloading'] if unload else 0

        cursor.execute("SELECT standard_waiting_charges FROM waiting_charges WHERE house_size = %s", (house_size,))
        wait = cursor.fetchone()
        wait_cost = wait['standard_waiting_charges'] if wait else 0

        cursor.execute("""
            SELECT base_intra, per_km_intra, base_inter, per_km_inter
            FROM transportation_charges
            WHERE house_size = %s AND vehicle = %s
        """, (house_size, vehicle))
        t = cursor.fetchone()
        if t:
            intra = t['base_intra'] + t['per_km_intra'] * max(0, distance - 10)
            inter = t['base_inter'] + t['per_km_inter'] * max(0, distance - 10)
        else:
            intra = inter = 0

        cursor.close()
        conn.close()

        result = f"""
🧾 Estimated Cost Breakdown for {house_size} (Intra-City):
    Packing: {packing_cost}
    Loading (Floor {floor_from}): {load_cost}
    Unloading (Floor {floor_to}): {unload_cost}
    Waiting (6 hrs): {wait_cost}
    Transport (Intra): {intra}
    ==============================================================================
    Total (Intra): Rs.{packing_cost + load_cost + unload_cost + wait_cost + intra}
    ==============================================================================

🧾 Estimated Cost Breakdown for {house_size} (Inter-City):
    Packing: {packing_cost}
    Loading (Floor {floor_from}): {load_cost}
    Unloading (Floor {floor_to}): {unload_cost}
    Waiting (6 hrs): {wait_cost}
    Transport (Inter): {inter}
    ==============================================================================
    Total (Inter): Rs.{packing_cost + load_cost + unload_cost + wait_cost + inter}
    ==============================================================================
"""
        return result
    except Exception as e:
        return f"❌ Error fetching estimation: {e}"