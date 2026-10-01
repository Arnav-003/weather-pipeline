{{ config(materialized='view') }}

select
    fetched_at,
    -- Maps your exact BigQuery 'readings' column to a clean timestamp name
    cast(readings as timestamp) as reading_timestamp, 
    temperature as temp_celsius,
    (temperature * 9/5) + 32 as temp_fahrenheit,
    windspeed as wind_speed_kmh,
    -- Maps your exact BigQuery spelling 'wethercode' to a clean name
    wethercode as weather_code
from {{ source('weather_raw', 'current_conditions') }}
