INSERT_OFFER = '''
                    INSERT INTO public.sku (
                        uuid,
                        marketplace_id,
                        product_id,
                        title,
                        description,
                        brand,
                        seller_id,
                        seller_name,
                        first_image_url,
                        category_id,
                        category_lvl_1,
                        category_lvl_2,
                        category_lvl_3,
                        category_remaining,
                        features,
                        rating_count,
                        rating_value,
                        price_before_discounts,
                        discount,
                        price_after_discounts,
                        bonuses,
                        sales,
                        inserted_at,
                        updated_at,
                        currency,
                        barcode
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26)
                '''

OFFER_UPDATE = """
        UPDATE sku
        SET similar_sku = $1
        WHERE uuid = $2
        """

GET_COUNT_OFFERS = """
    SELECT COUNT(*) FROM sku
"""

SELECT_UUID_FROM_OFFERS = """
    SELECT uuid FROM sku ORDER BY uuid OFFSET $1 LIMIT $2
"""