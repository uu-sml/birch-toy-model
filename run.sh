birch build --disable-debug
birch install
birch sample --config=config/toy_model_pmmh_small.json
python parsedata.py
