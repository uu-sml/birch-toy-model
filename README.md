# pgibbs-toy-model
Birch implementation of the toy model (Andrieu, 2010)

Build and install
```
birch build
birch install
```

Sample the original toy model using
```
birch sample --config=config/toy_model.json --input=input/toy_model.json --output=output/toy_model.json
```

Sample the marginalized version
```
birch sample --config=config/marginalized_toy_model.json --input=input/toy_model.json --output=output/marginalized_toy_model.json
```
