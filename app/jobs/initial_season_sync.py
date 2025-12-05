from app.db.session import SessionLocal
import requests
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from app.config import settings
from app.db.models.match_model import Match

def get_season_match_data(competition_ids: list[int], league_season: int, match_status: str = "SCHEDULED"):
    db = SessionLocal()
    try:
        for cid in competition_ids:
            uri = f"https://api.football-data.org/v4/competitions/{cid}/matches"
            headers = { 'X-Auth-Token': settings.football_data_api_key }
            params = { "season": league_season, "status": match_status }

            resp = requests.get(uri, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            fil = data.get("filters", {})
            competition = data.get("competition", {})
            matches = data.get("matches", [])

            for match in matches:
                kickoff_str = match.get("utcDate")
                kickoff = datetime.fromisoformat(kickoff_str.replace("Z", "+00:00")) if kickoff_str else None

                match_data = {
                    "season": fil.get("season"),
                    "league": competition.get("name"),
                    "league_code": competition.get("code"),
                    "competition_logo": competition.get("emblem"),
                    "country": match.get("area", {}).get("name"),
                    "country_flag": match.get("area", {}).get("flag"),
                    "country_code": match.get("area", {}).get("code"),
                    "api_match_id": match.get("id"),
                    "status": match.get("status"),
                    "kickoff": kickoff,
                    "home_team": match.get("homeTeam", {}).get("shortName"),
                    "home_logo": match.get("homeTeam", {}).get("crest"),
                    "away_team": match.get("awayTeam", {}).get("shortName"),
                    "away_logo": match.get("awayTeam", {}).get("crest"),
                    "home_score": match.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": match.get("score", {}).get("fullTime", {}).get("away"),
                    "winner": match.get("score", {}).get("winner"),
                }

                stmt = insert(Match).values(**match_data).on_conflict_do_update(
                    index_elements=["api_match_id"],
                    set_=match_data
                )
                db.execute(stmt)

            db.commit()

    finally:
        db.close()

    return {"Success": "Matches Added"}
