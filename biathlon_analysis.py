import pandas as pd
import numpy as np
from datetime import datetime

def main():
    """Main analysis function for Swiss Olympic Biathlon data"""
    
    print("🏔️ SWISS OLYMPIC BIATHLON ANALYSIS")
    print("=" * 50)
    
    # Load the data
    file_path = "Results_Test_Version.csv"
    
    try:
        # Load the CSV with semicolon separator
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # Clean column names (remove quotes)
        df.columns = df.columns.str.strip('"')
        
        # Convert date columns
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
        df['DoB'] = pd.to_datetime(df['DoB'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['Year', 'Rank', '# Participants', '# Countries', '# Continents', 'Age']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Clean rank column - handle special values like 'DNS', 'DNF'
        df['Rank_Clean'] = pd.to_numeric(df['Rank'], errors='coerce')
        
        # Add season column (biathlon season runs roughly Nov-Mar)
        df['Season'] = df['Date'].apply(lambda x: f"{x.year-1}/{x.year}" if x.month <= 6 else f"{x.year}/{x.year+1}")
        
        # Filter for biathlon results only
        df_all = df.copy()  # Keep all sports for reference
        df = df[df['Sport'] == 'Biathlon'].copy()
        
        print("✅ Data loaded and cleaned successfully!")
        print(f"📊 Filtered to {len(df)} biathlon results from {len(df_all)} total results")
        
        # Basic Statistics
        print("\n📊 BASIC DATASET STATISTICS")
        print("-" * 30)
        print(f"Total records: {len(df):,}")
        print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
        print(f"Number of unique athletes: {df['Person'].nunique()}")
        print(f"Number of competitions: {df['Competition'].nunique()}")
        
        # Athletes Analysis
        print("\n🏃‍♂️ ATHLETES OVERVIEW")
        print("-" * 20)
        athletes = df.groupby(['Person', 'PersonGender']).size().reset_index(name='Races')
        athletes = athletes.sort_values('Races', ascending=False)
        
        print("Top 10 athletes by number of races:")
        for _, athlete in athletes.head(10).iterrows():
            print(f"  {athlete['Person']} ({athlete['PersonGender']}): {athlete['Races']} races")
        
        men_count = len(athletes[athletes['PersonGender'] == 'Men'])
        women_count = len(athletes[athletes['PersonGender'] == 'Women'])
        print(f"\nGender distribution:")
        print(f"  Men: {men_count} athletes")
        print(f"  Women: {women_count} athletes")
        
        # Competition Analysis
        print("\n🏆 COMPETITION ANALYSIS")
        print("-" * 22)
        comp_types = df['Comp.SetDetail'].value_counts()
        print("Competition types:")
        for comp, count in comp_types.items():
            print(f"  {comp}: {count} results")
        
        print(f"\nDisciplines:")
        disciplines = df['Discipline'].value_counts()
        for disc, count in disciplines.head(8).items():
            print(f"  {disc}: {count} results")
        
        print(f"\nSeasons:")
        seasons = df['Season'].value_counts().sort_index()
        for season, count in seasons.items():
            print(f"  {season}: {count} results")
        
        # Performance Analysis
        df_ranked = df[df['Rank_Clean'].notna() & (df['Rank_Clean'] > 0)]
        
        print("\n🥇 PERFORMANCE ANALYSIS")
        print("-" * 22)
        best_ranks = df_ranked.groupby('Person')['Rank_Clean'].min().sort_values()
        print("Best ever rankings (Top 10):")
        for athlete, rank in best_ranks.head(10).items():
            print(f"  {athlete}: Rank {int(rank)}")
        
        # Podium finishes (Top 3)
        podiums = df_ranked[df_ranked['Rank_Clean'] <= 3]
        print(f"\n🏅 Podium finishes: {len(podiums)}")
        
        if len(podiums) > 0:
            podium_summary = podiums.groupby(['Person', 'Rank_Clean']).size().unstack(fill_value=0)
            print("Podium breakdown by athlete:")
            for athlete in podium_summary.index:
                wins = podium_summary.loc[athlete, 1] if 1 in podium_summary.columns else 0
                second = podium_summary.loc[athlete, 2] if 2 in podium_summary.columns else 0  
                third = podium_summary.loc[athlete, 3] if 3 in podium_summary.columns else 0
                total = wins + second + third
                if total > 0:
                    print(f"  {athlete}: {wins} wins, {second} 2nd, {third} 3rd (Total: {total})")
        
        # Top 10 finishes
        top10 = df_ranked[df_ranked['Rank_Clean'] <= 10]
        print(f"\n🔟 Top 10 finishes: {len(top10)}")
        top10_by_athlete = top10.groupby('Person').size().sort_values(ascending=False)
        print("Top 10 finishes by athlete (Top 5):")
        for athlete, count in top10_by_athlete.head(5).items():
            print(f"  {athlete}: {count}")
        
        # Olympic Qualification Preview
        print("\n🎯 OLYMPIC QUALIFICATION PREVIEW")
        print("-" * 32)
        
        # World Championships 2025 results
        wc_2025 = df_ranked[
            (df_ranked['Comp.SetDetail'] == 'IBU World Championships') & 
            (df_ranked['Year'] == 2025)
        ]
        
        print(f"World Championships 2025 results: {len(wc_2025)}")
        
        # Top 3 at WC 2025 (Route 1 qualification path)
        wc_2025_podium = wc_2025[wc_2025['Rank_Clean'] <= 3]
        if len(wc_2025_podium) > 0:
            print("🥇 Top-3 at World Championships 2025 (Route 1 candidates):")
            for _, result in wc_2025_podium.iterrows():
                print(f"  {result['Person']}: Rank {int(result['Rank_Clean'])} in {result['Discipline']}")
        
        # World Cup 2025/26 season (future data for testing)
        wc_future = df_ranked[
            (df_ranked['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (df_ranked['Date'] >= '2025-11-01')
        ]
        print(f"\nWorld Cup 2025/26 season results: {len(wc_future)}")
        
        # Save cleaned data
        output_file = "cleaned_biathlon_results.csv"
        df.to_csv(output_file, index=False)
        print(f"\n💾 Cleaned data saved to: {output_file}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    df = main()
    
    if df is not None:
        print(f"\n✅ Analysis complete! Dataset shape: {df.shape}")
        print("Next steps:")
        print("  1. Run detailed qualification checks")
        print("  2. Generate athlete-specific reports")
        print("  3. Create visualization dashboards")
