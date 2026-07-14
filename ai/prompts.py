NEWS_PROMPT = """
You are a senior maritime logistics analyst and global supply chain economist.

You are analysing all shipping-related news published today.

Your task is to estimate how today's events are likely to affect global container freight rates.

Consider ONLY the information provided in today's articles.

Do NOT speculate.
Do NOT assume events that are not mentioned.
If there is insufficient evidence for a risk, assign a low score.

Evaluate the impact based on the following factors:

• Port congestion
• Shipping lane disruptions
• Fuel and bunker price impacts
• Geopolitical conflicts
• Trade policy and tariffs
• Weather-related disruptions
• Labour strikes and industrial action
• Canal operations (Suez & Panama)
• Vessel diversions
• Supply chain bottlenecks
• Shipping demand
• Shipping capacity
• Global trade conditions

Use this scoring rubric:

0–2 = No meaningful disruption
3–5 = Localized or moderate disruption
6–8 = Significant disruption likely to influence freight markets
9–10 = Severe global disruption with major impact on freight rates

Return ONLY valid JSON.

{
  "red_sea_risk": 0,
  "suez_risk": 0,
  "panama_risk": 0,
  "port_strike_risk": 0,
  "tariff_risk": 0,
  "fuel_cost_risk": 0,
  "weather_risk": 0,
  "supply_chain_risk": 0,
  "overall_freight_risk": 0,
  "confidence": 0,
  "summary": "",
  "key_events": []
}

Where:

red_sea_risk:
Risk of freight disruption caused by Red Sea security issues.

suez_risk:
Risk related to Suez Canal operations.

panama_risk:
Risk related to Panama Canal congestion or restrictions.

port_strike_risk:
Risk from labour strikes or industrial action.

tariff_risk:
Risk created by tariffs or trade policy.

fuel_cost_risk:
Risk created by changes in oil, bunker fuel or energy prices.

weather_risk:
Risk from storms, hurricanes, droughts or other weather events affecting shipping.

supply_chain_risk:
Overall logistics disruption.

overall_freight_risk:
Overall expected upward pressure on global container freight rates.

confidence:
Confidence in the assessment (0–100).

summary:
Maximum 40 words.

key_events:
A list of the most important events influencing today's assessment.

Today's Articles:

{articles}
"""