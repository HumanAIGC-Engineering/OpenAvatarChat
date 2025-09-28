#!/usr/bin/env bash

# Build script for OpenAvatarChat Docker images
# Usage: ./scripts/build-docker.sh [avatar|lam|both] [tag_suffix]

set -e

# Default values
IMAGE_TYPE="${1:-both}"
TAG_SUFFIX="${2:-latest}"
REGISTRY="${REGISTRY:-ghcr.io}"
REPO_NAME="${REPO_NAME:-$(basename $(git rev-parse --show-toplevel))}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build Docker image
build_image() {
    local config_file=$1
    local image_name=$2
    local image_tag=$3
    
    print_status "Building $image_name with config: $config_file"
    
    if ! docker build \
        --build-arg CONFIG_FILE="$config_file" \
        -t "$image_tag" \
        -f Dockerfile \
        .; then
        print_error "Failed to build $image_name"
        return 1
    fi
    
    print_success "Successfully built $image_name -> $image_tag"
    return 0
}

# Function to push image to registry
push_image() {
    local image_tag=$1
    local image_name=$2
    
    print_status "Pushing $image_name to registry..."
    
    if ! docker push "$image_tag"; then
        print_error "Failed to push $image_name"
        return 1
    fi
    
    print_success "Successfully pushed $image_name"
    return 0
}

# Main script
main() {
    print_status "Starting Docker build process..."
    print_status "Image Type: $IMAGE_TYPE"
    print_status "Tag Suffix: $TAG_SUFFIX"
    print_status "Registry: $REGISTRY"
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Check if required config files exist
    if [[ "$IMAGE_TYPE" == "avatar" || "$IMAGE_TYPE" == "both" ]]; then
        if [[ ! -f "config/chat_with_dify.yaml" ]]; then
            print_error "Avatar config file not found: config/chat_with_dify.yaml"
            exit 1
        fi
    fi
    
    if [[ "$IMAGE_TYPE" == "lam" || "$IMAGE_TYPE" == "both" ]]; then
        if [[ ! -f "config/chat_with_lam_dify.yaml" ]]; then
            print_error "LAM config file not found: config/chat_with_lam_dify.yaml"
            exit 1
        fi
    fi
    
    # Build Avatar image
    if [[ "$IMAGE_TYPE" == "avatar" || "$IMAGE_TYPE" == "both" ]]; then
        AVATAR_TAG="$REGISTRY/$REPO_NAME-avatar:$TAG_SUFFIX"
        if build_image "config/chat_with_dify.yaml" "Avatar (Dify)" "$AVATAR_TAG"; then
            print_status "Avatar image built successfully"
            
            # Ask if user wants to push
            read -p "Do you want to push Avatar image to registry? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                push_image "$AVATAR_TAG" "Avatar (Dify)"
            fi
        else
            print_error "Avatar image build failed"
            exit 1
        fi
    fi
    
    # Build LAM image
    if [[ "$IMAGE_TYPE" == "lam" || "$IMAGE_TYPE" == "both" ]]; then
        LAM_TAG="$REGISTRY/$REPO_NAME-lam:$TAG_SUFFIX"
        if build_image "config/chat_with_lam_dify.yaml" "LAM (Dify)" "$LAM_TAG"; then
            print_status "LAM image built successfully"
            
            # Ask if user wants to push
            read -p "Do you want to push LAM image to registry? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                push_image "$LAM_TAG" "LAM (Dify)"
            fi
        else
            print_error "LAM image build failed"
            exit 1
        fi
    fi
    
    print_success "All builds completed successfully!"
    
    # Show built images
    print_status "Built images:"
    if [[ "$IMAGE_TYPE" == "avatar" || "$IMAGE_TYPE" == "both" ]]; then
        echo "  - $REGISTRY/$REPO_NAME-avatar:$TAG_SUFFIX"
    fi
    if [[ "$IMAGE_TYPE" == "lam" || "$IMAGE_TYPE" == "both" ]]; then
        echo "  - $REGISTRY/$REPO_NAME-lam:$TAG_SUFFIX"
    fi
}

# Help function
show_help() {
    echo "Usage: $0 [IMAGE_TYPE] [TAG_SUFFIX]"
    echo ""
    echo "Arguments:"
    echo "  IMAGE_TYPE    Type of image to build (avatar|lam|both) [default: both]"
    echo "  TAG_SUFFIX    Tag suffix for the images [default: latest]"
    echo ""
    echo "Environment Variables:"
    echo "  REGISTRY      Docker registry URL [default: ghcr.io]"
    echo "  REPO_NAME     Repository name [default: current directory name]"
    echo ""
    echo "Examples:"
    echo "  $0                          # Build both images with 'latest' tag"
    echo "  $0 avatar                   # Build only avatar image"
    echo "  $0 lam v1.0.0              # Build only LAM image with v1.0.0 tag"
    echo "  $0 both dev                 # Build both images with 'dev' tag"
    echo ""
    echo "  REGISTRY=docker.io $0       # Use Docker Hub instead of GitHub Container Registry"
}

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Validate IMAGE_TYPE
if [[ "$IMAGE_TYPE" != "avatar" && "$IMAGE_TYPE" != "lam" && "$IMAGE_TYPE" != "both" ]]; then
    print_error "Invalid image type: $IMAGE_TYPE"
    print_error "Valid options: avatar, lam, both"
    exit 1
fi

# Run main function
main
