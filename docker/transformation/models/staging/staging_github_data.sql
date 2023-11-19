-- remove duplicates 

{{ 
  config(
    materialized = 'table',
  ) 
}}

WITH ranked AS (
    SELECT id, 
        type, 
        actor, 
        repo,
        payload,
        public, 
        created_at, 
        org,
        ROW_NUMBER() OVER (
        PARTITION BY id
        ORDER BY created_at DESC NULLS LAST
        ) AS __rank
    FROM {{ source('staging', 'github_data') }}
)
SELECT id, 
    type, 
    actor, 
    repo,
    payload,
    public, 
    created_at, 
    org
FROM ranked
WHERE __rank = 1
