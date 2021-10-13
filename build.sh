#!/bin/bash

build () {

    # check for the type of OS 
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then 

        # remove production file if exists
        if [ -d "$1-auth" ]; then 
            sudo rm -r $1-auth
        fi

        # create production folder contents
        sudo mkdir $1-auth
        sudo cp -r nginx $1-auth/
        sudo cp docker-compose.yml $1-auth/
        sudo cp run.sh $1-auth/

        # its linux
        if [[ $1 == test ]]; then 
            _rev="janjas/auth"
            _put="janjas/$1-auth"
            _name="auth"
            _newname="$1-auth"
            
            sudo sed -i "s|$_rev|$_put|g" $1-auth/docker-compose.yml
            sudo sed -i "s|$_rev|$_put|g" $1-auth/run.sh
            sudo sed -i "s|$_name|$_newname|g" $1-auth/nginx/nginx.conf
            sudo sed -i "s|$_name|$_newname|g" $1-auth/docker-compose.yml
            sudo sed -i "s|$_name|$_newname|g" .github/workflows/deploy-test.yml
            sudo sed -i "s|$_name|$_newname|g" .github/workflows/deploy-prod.yml

            # since it created double $1-$1 on the image, remove that
            _double_name="$1-$1-auth"
            _singlename="$1-auth"

            sudo sed -i "s|$_double_name|$_singlename|g" $1-auth/docker-compose.yml

            # build
            sudo docker build -t janjas/$1-auth src/
        else 

            # build
            sudo docker build -t janjas/auth src/
        fi
    else

        # remove production file if exists
        if [ -d "$1-auth" ]; then 
            rm -r $1-auth
        fi

        mkdir $1-auth
        cp -r nginx $1-auth/
        cp docker-compose.yml $1-auth/
        cp run.sh $1-auth/

        # its windows
        if [[ $1 == test ]]; then 
            _rev="janjas/auth"
            _put="janjas/$1-auth"
            _name="auth"
            _newname="$1-auth"

            sed -i "s|$_rev|$_put|g" $1-auth/docker-compose.yml
            sed -i "s|$_rev|$_put|g" $1-auth/run.sh
            sed -i "s|$_name|$_newname|g" $1-auth/nginx/nginx.conf
            sed -i "s|$_name|$_newname|g" $1-auth/docker-compose.yml
            sed -i "s|$_name|$_newname|g" .github/workflows/deploy-test.yml
            sed -i "s|$_name|$_newname|g" .github/workflows/deploy-prod.yml

            # since it created double $1-$1 on the image, remove that
            _double_name="$1-$1-auth"
            _singlename="$1-auth"

            sed -i "s|$_double_name|$_singlename|g" $1-auth/docker-compose.yml

            # build
            docker build -t janjas/$1-auth src/
        else 
            
            # build
            docker build -t janjas/auth src/
        fi

    fi

}


# running tasks
if [[ $1 == "prod" ]]; then
    echo "Building for production"
    build "prod"
elif [[ $1 == "test" ]]; then
    echo "Building for testing"
    build "test"
else 
    echo
    echo "-------------"
    echo "specify if you are building for production or test"
    echo "syntax: ./build.sh [type]"
    echo "[type] - prod or test"
fi

