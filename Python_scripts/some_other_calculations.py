# Tables with ADTs (cut from the main app)




### table with critical ADTs (flows)
st.markdown('###### Critical road cross-sectional ADT [pc/24h]')
   
df_crit_adt = pd.DataFrame(
        {
        "PSR A": [round(2* lanes * bs.calculate_metrics_at_density(6.5)[1]/bs.define_u50(), -3)],
        "PSR B": [round(2* lanes * bs.calculate_metrics_at_density(11)[1]/bs.define_u50(), -3)],
        "PSR C": [round(2* lanes * bs.calculate_metrics_at_density(16)[1]/bs.define_u50(), -3)],
        "PSR D": [round(2* lanes * bs.calculate_metrics_at_density(21)[1]/bs.define_u50(), -3)],
        "PSR E": [round(2* lanes * bs.calculate_metrics_at_density(26.5)[1]/bs.define_u50(), -3)],
        }
    )
st.dataframe(df_crit_adt, hide_index=True)

    ### table with critical ADTs (volumes)
st.markdown('###### Critical road cross-sectional ADT [veh/24h]')
   
df_crit_adt = pd.DataFrame(
        {
        "PSR A": [round(bs.calculate_k15() * 2* lanes * bs.calculate_metrics_at_density(6.5)[1]/(bs.define_u50() * bs.calculate_ew()), -3)],
        "PSR B": [round(bs.calculate_k15() * 2* lanes * bs.calculate_metrics_at_density(11)[1]/(bs.define_u50() * bs.calculate_ew()), -3)],
        "PSR C": [round(bs.calculate_k15() * 2* lanes * bs.calculate_metrics_at_density(16)[1]/(bs.define_u50() * bs.calculate_ew()), -3)],
        "PSR D": [round(bs.calculate_k15() * 2* lanes * bs.calculate_metrics_at_density(21)[1]/(bs.define_u50() * bs.calculate_ew()), -3)],
        "PSR E": [round(bs.calculate_k15() * 2* lanes * bs.calculate_metrics_at_density(26.5)[1]/(bs.define_u50() * bs.calculate_ew()), -3)],
        }
    )
st.dataframe(df_crit_adt, hide_index=True)