{{ config(materialized='view') }}

select
    fetched_at,
        -- Safely reads the text format 'YYYY-MM-DDTHH:MM' from the API
    parse_timestamp('%Y-%m-%dT%H:%M', readings) as reading_timestamp, 
    temperature as temp_celsius,
    (temperature * 9/5) + 32 as temp_fahrenheit,
    windspeed as wind_speed_kmh,
    -- Maps your exact BigQuery spelling 'wethercode' to a clean name
    wethercode as weather_code
from {{ source('weather_raw', 'current_conditions') }}
