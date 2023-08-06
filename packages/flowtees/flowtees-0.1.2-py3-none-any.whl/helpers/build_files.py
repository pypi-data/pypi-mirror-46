
def get_template_build_tsconfig() -> str:
    tsconfig = '''
    {
        "extends": "../../tsconfig",
        "compilerOptions": {
            "declaration": true,
            "outDir": "../../",
            "target": "es5",
            "module": "esnext",
            "paths": {}
        },
        "include": [
            "../../src/**/*.ts",
            "../../src/**/*.tsx"
        ],
        "exclude": ["../../src/**/__tests__/*"]
    }'''
    return tsconfig


def get_template_base_tsconfig() -> str:
    tsconfig = '''
    {
        "extends": "../../../tsconfig.core.json",
        "include": [
            "./src/**/*.ts",
            "./src/**/*.tsx",
            "./docs/**/*.ts",
            "./docs/**/*.tsx",
            "./examples/**/*.ts",
            "./examples/**/*.tsx",
            "./example-helpers/**/*.ts",
            "./example-helpers/**/*.tsx"
        ],
        "compilerOptions": {
            "baseUrl": "./"
        }
    }'''
    return tsconfig
