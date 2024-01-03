mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = 'joseph@eagerdata.com'\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[theme]\n\
base = 'light'
" > ~/.streamlit/config.toml