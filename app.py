import json
import os
import yt_dlp
import streamlit as st

# Config yönetimi
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "mp3_dir": "",
            "mp4_dir": "",
            "m4a_dir": ""
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Format seçici fonksiyonu
def format_selector(ctx):
    formats = ctx.get('formats')[::-1]
    best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
    
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

# Temel yapılandırmalar
base_ydl_opts = {
    "m4a": {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
    },
    "mp3": {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0'
        }],
    },
    "mp4": {
        'format': format_selector,
    }
}

def main():
    st.set_page_config(page_title="MediaDownloader", page_icon="🎵")
    st.title("MediaDownloader 🎵")
    
    # Config yükle
    config = load_config()
    
    # Klasör seçim arayüzü
    with st.expander("⚙️ Klasör Ayarları", expanded=True):
        st.write("### Formatlara Özel Klasör Yolları")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            mp3_dir = st.text_input(
                "MP3 Klasörü", 
                value=config.get("mp3_dir", ""),
                help="MP3 dosyalarının kaydedileceği tam yol"
            )
        with col2:
            mp4_dir = st.text_input(
                "MP4 Klasörü", 
                value=config.get("mp4_dir", ""),
                help="MP4 dosyalarının kaydedileceği tam yol"
            )
        with col3:
            m4a_dir = st.text_input(
                "M4A Klasörü", 
                value=config.get("m4a_dir", ""),
                help="M4A dosyalarının kaydedileceği tam yol"
            )
        
        if st.button("💾 Ayarları Kaydet"):
            new_config = {
                "mp3_dir": mp3_dir,
                "mp4_dir": mp4_dir,
                "m4a_dir": m4a_dir
            }
            save_config(new_config)
            st.success("Ayarlar başarıyla kaydedildi!")

    
    url = st.text_input("Medya Linki", placeholder="Lütfen medya linkini yapıştırın")
    
    # Format seçim state yönetimi
    if 'selected_format' not in st.session_state:
        st.session_state.selected_format = None

    selected = st.radio(
        "📁 İndirme Formatını Seçin:",
        options=["mp3", "mp4", "m4a"],
        index=None,
        horizontal=True
    )
    st.session_state.selected_format = selected
    
    # İndirme butonu
    if st.session_state.selected_format and url:
        if st.button("🚀 İndirmeyi Başlat", type="primary"):
            try:
                format_type = st.session_state.selected_format
                download_dir = config.get(f"{format_type}_dir", "")
                
                if not download_dir:
                    st.error(f"Lütfen önce {format_type.upper()} klasör yolunu ayarlayın!")
                    return
                
                os.makedirs(download_dir, exist_ok=True)
                
                # Yapılandırmayı hazırla
                options = base_ydl_opts[format_type].copy()
                options["outtmpl"] = os.path.join(
                    download_dir, 
                    f"%(title)s.%(ext)s"
                )

                with st.spinner(f"{format_type.upper()} indiriliyor..."):
                    with yt_dlp.YoutubeDL(options) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'bilinmeyen_başlık')
                        
                st.success(f"✅ {format_type.upper()} indirme tamamlandı: {title}")
                st.balloons()

                # İndirilen dosya yolunu göster
                file_ext = 'mp3' if format_type == 'mp3' else format_type
                file_path = os.path.join(download_dir, f"{title}.{file_ext}")
                st.code(f"Kayıt Yolu: {file_path}", language="bash")

            except Exception as e:
                st.error(f"❌ Hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()