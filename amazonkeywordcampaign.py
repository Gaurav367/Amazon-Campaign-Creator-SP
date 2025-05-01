import pandas as pd
from datetime import datetime
import os
import time

class AmazonCampaignBuilder:
    def __init__(self):
        self.FIXED_VALUES = {
            'Product': 'Sponsored Products',
            'Operation': 'Create',
            'Targeting Type': 'Manual',
            'State': 'Enabled'
        }
        self.VALID_KEYWORD_MATCH_TYPES = ['exact', 'phrase', 'broad']
        self.VALID_NEGATIVE_MATCH_TYPES = ['negativeExact', 'negativePhrase']

    def create_campaign_structure(self, input_data):
        """Creates campaign structure: campaign, bidding adj, ad group, product ads, keywords, negative keywords"""
        all_rows = []
        for _, row in input_data.iterrows():
            # Input fields
            campaign_id = row.get('campaign_name', '')
            portfolio_id = row.get('portfolio_id', '')
            budget = row.get('budget', '')
            ad_group_bid = row.get('ad_group_default_bid', '')
            skus = self._parse_list_field(row.get('sku', ''))
            asin = row.get('asin', '')
            start_date = row.get('start_date', '')
            end_date = row.get('end_date', '')
            keywords = self._parse_list_field(row.get('keyword_text', ''))
            kmatch = str(row.get('keyword_match_type', '')).strip().lower()
            negs = self._parse_list_field(row.get('negative_keyword_text', ''))
            neg_match = str(row.get('negative_match_type', '')).strip()
            bid = row.get('bid', '')
            strat = str(row.get('bidding_strategy', '')).strip()
            placement = str(row.get('placement', '')).strip()
            pct = row.get('percentage', '')
            pt_expr = row.get('product_targeting_expression', '')

            # Base for every row
            base = {**self.FIXED_VALUES,
                    'Campaign Id': campaign_id,
                    'Campaign Name': campaign_id,
                    'Ad Group Id': campaign_id,
                    'Ad Group Name': campaign_id,
                    'Portfolio Id': portfolio_id,
                    'Start Date': start_date,
                    'End Date': end_date,
                    'ASIN (Informational only)': asin,
                    'Product Targeting Expression': pt_expr}

            # 1. Campaign
            row_campaign = {**base, 'Entity':'Campaign', 'Daily Budget': budget, 'Bidding Strategy': strat}
            all_rows.append(row_campaign)
            
            # 2. Bidding Adjustment - only add if placement and percentage are not empty
            if placement and (pct is not None and pct != ''):
                row_adj = {**base, 'Entity':'Bidding Adjustment', 'Bidding Strategy': strat,
                        'Placement': placement, 'Percentage': pct}
                all_rows.append(row_adj)
                
            # 3. Ad Group
            row_ag = {**base, 'Entity':'Ad Group', 'Ad Group Default Bid': ad_group_bid}
            all_rows.append(row_ag)
            # 4. Product Ads
            for sku in skus:
                row_pa = {**base, 'Entity':'Product ad', 'SKU': sku}
                all_rows.append(row_pa)
            # 5. Keywords
            if kmatch in self.VALID_KEYWORD_MATCH_TYPES:
                for kw in keywords:
                    row_kw = {**base, 'Entity':'Keyword', 'Bid': bid,
                              'Keyword Text': kw, 'Match Type': kmatch}
                    all_rows.append(row_kw)
            # 6. Negative Keywords
            if neg_match in self.VALID_NEGATIVE_MATCH_TYPES:
                for nk in negs:
                    row_nk = {**base, 'Entity':'Negative Keyword',
                              'Keyword Text': nk, 'Match Type': neg_match}
                    all_rows.append(row_nk)

        df = pd.DataFrame(all_rows)
        cols = [
            'Product','Entity','Operation','Campaign Id','Campaign Name','Ad Group Id','Ad Group Name',
            'Portfolio Id','Ad Id (Read only)','Keyword Id (Read only)','Product Targeting Id (Read only)',
            'Start Date','End Date','Targeting Type','State','Daily Budget','SKU','ASIN (Informational only)',
            'Ad Group Default Bid','Bid','Keyword Text','Match Type','Bidding Strategy','Placement',
            'Percentage','Product Targeting Expression'
        ]
        for c in cols:
            if c not in df.columns:
                df[c] = ''
        return df[cols]

    def _parse_list_field(self, field):
        if pd.isna(field) or field == '': return []
        if isinstance(field, str):
            sep = ',' if ',' in field else ';' if ';' in field else None
            return [i.strip() for i in field.split(sep)] if sep else [field.strip()]
        return [str(field)]

# Excel I/O and pipeline

def safe_file_write_excel(df, filepath, max_attempts=5):
    for i in range(max_attempts):
        try:
            
            df.to_excel(filepath, index=False)
            return True
        except PermissionError:
            if i < max_attempts-1: time.sleep(2)
            else:
                b, _ = os.path.splitext(filepath)
                alt = f"{b}_{datetime.now().strftime('%H%M%S')}.xlsx"
                df.to_excel(alt, index=False)
                return True
        except:
            return False
    return False


def create_output_directory():
    out = os.path.join(os.getcwd(), "amazon_campaign_output_Manual")
    os.makedirs(out, exist_ok=True)
    return out


def process_bulk_file(input_file_path):
    if not os.path.exists(input_file_path):
        print(f"Error: '{input_file_path}' not found.")
        return False
    try:
        data = pd.read_excel(input_file_path, na_filter=False)
    except Exception as e:
        print(f"Read failed: {e}")
        return False
    out = AmazonCampaignBuilder().create_campaign_structure(data)
    od = create_output_directory()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    fn = os.path.join(od, f"amazon_bulk_campaign_{ts}.xlsx")
    if safe_file_write_excel(out, fn):
        print(f"Generated: {fn}")
        return True
    print("Save failed.")
    return False

if __name__ == "__main__":
    path = r"Input Multi Keyword.xlsx"
    print("Processing Excel input...")
    process_bulk_file(path)