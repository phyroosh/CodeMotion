"""
YouTube Data API v3 Direct Uploader.
Uploads videos with metadata and posts automated pinned comments.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

DEFAULT_CREDENTIALS_DIR = Path(__file__).resolve().parent.parent / "credentials"
RIGHTCLIPS_SECRETS = Path("/home/phyroosh/TopProducts/RightClips/studio/client_secrets.json")


def get_youtube_service(client_secrets_path: Optional[str] = None, token_path: Optional[str] = None):
    """
    Authenticates and returns the authorized YouTube Data API service.
    """
    DEFAULT_CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Resolve token path
    if token_path:
        t_path = Path(token_path)
    else:
        t_path = DEFAULT_CREDENTIALS_DIR / "token.json"

    creds = None
    if t_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(t_path), SCOPES)
        except Exception as e:
            print(f"⚠️ Error reading existing token: {e}")

    # 2. Refresh or trigger flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Resolve client secrets
            if client_secrets_path and Path(client_secrets_path).exists():
                s_path = Path(client_secrets_path)
            elif (DEFAULT_CREDENTIALS_DIR / "client_secrets.json").exists():
                s_path = DEFAULT_CREDENTIALS_DIR / "client_secrets.json"
            elif RIGHTCLIPS_SECRETS.exists():
                print(f"🔑 Using existing client_secrets.json found in RightClips: {RIGHTCLIPS_SECRETS}")
                s_path = RIGHTCLIPS_SECRETS
            else:
                raise FileNotFoundError(
                    "❌ client_secrets.json not found!\n"
                    "Please place your Google Cloud OAuth client_secrets.json into:\n"
                    f"  {DEFAULT_CREDENTIALS_DIR / 'client_secrets.json'}\n"
                    "Or use the RightClips bridge export to publish via RightClips Studio."
                )

            flow = InstalledAppFlow.from_client_secrets_file(str(s_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next runs
        with open(t_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"💾 Saved YouTube authentication token to: {t_path}")

    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(
    video_path: str,
    metadata: Dict[str, Any],
    client_secrets_path: Optional[str] = None,
    token_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Uploads a video to YouTube with title, description, tags, and category.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    youtube = get_youtube_service(client_secrets_path, token_path)

    body = {
        "snippet": {
            "title": metadata.get("title", "Autonomous Video #Shorts"),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", ["Shorts", "Tech"]),
            "categoryId": str(metadata.get("categoryId", "28")),
        },
        "status": {
            "privacyStatus": metadata.get("privacyStatus", "public"),
            "selfDeclaredMadeForKids": False,
        },
    }

    print(f"🚀 Uploading {video_path} to YouTube...")
    print(f"📌 Title: {body['snippet']['title']}")

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⏳ Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    shorts_url = f"https://youtube.com/shorts/{video_id}"
    watch_url = f"https://youtu.be/{video_id}"
    print(f"🎉 Upload Complete! Video ID: {video_id}")
    print(f"🔗 YouTube Shorts: {shorts_url}")

    # Optional: Post pinned comment
    pinned_comment = metadata.get("pinnedComment")
    comment_id = None
    if pinned_comment and video_id:
        try:
            comment_res = youtube.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": pinned_comment
                            }
                        }
                    }
                }
            ).execute()
            comment_id = comment_res.get("id")
            print(f"💬 Pinned Comment posted: {pinned_comment[:50]}...")
        except Exception as e:
            print(f"⚠️ Could not post comment: {e}")

    return {
        "videoId": video_id,
        "shortsUrl": shorts_url,
        "watchUrl": watch_url,
        "commentId": comment_id,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Direct Uploader")
    parser.add_argument("--video", required=True, help="Path to video MP4 file")
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON file")
    parser.add_argument("--secrets", default=None, help="Path to client_secrets.json")
    args = parser.parse_args()

    with open(args.metadata, "r", encoding="utf-8") as f:
        meta = json.load(f)

    upload_to_youtube(args.video, meta, client_secrets_path=args.secrets)
