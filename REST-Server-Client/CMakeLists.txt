cmake_minimum_required(VERSION 3.28)
project(rest-api)

# Find the Libraries
find_package(Crow REQUIRED)

# Link Source Files
add_executable(${PROJECT_NAME}
    src/main.cpp
    src/server/server.cpp
    src/server/handlers/base.cpp
    src/server/handlers/users.cpp
    src/server/handlers/products.cpp
)

# Link Libraries
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Crow::Crow
)

# Link Header Files (Include Dir)
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
)