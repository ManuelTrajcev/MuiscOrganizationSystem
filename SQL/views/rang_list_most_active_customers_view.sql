CREATE  VIEW rank_list_most_active_customers_view AS
SELECT
    c.first_name || ' ' || c.last_name as name,
    COUNT(i.invoice_id) as total_orders,
    SUM(i.total) as total_money_spent
from customer c
LEFT JOIN invoice i on c.customer_id = i.customer_id
where c.deleted_at is null
GROUP BY c.first_name, c.last_name
order by total_money_spent desc