from app.database.connection import get_connection


def create_tables():
    # 1. Connect to MariaDB
    connection = get_connection()
    cursor = connection.cursor()


    # 2. Create pets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            type VARCHAR(50) NOT NULL,
            breed VARCHAR(100),
            age INT,
            owner_name VARCHAR(100)
        )
    """)


    # 3. Create rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_number VARCHAR(20) NOT NULL UNIQUE,
            room_type VARCHAR(50) NOT NULL,
            daily_rate DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) NOT NULL
        )
    """)


    # 4. Create bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pet_id INT NOT NULL,
            room_id INT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            status VARCHAR(20) NOT NULL,


            FOREIGN KEY (pet_id)
                REFERENCES pets(id),


            FOREIGN KEY (room_id)
                REFERENCES rooms(id)
        )
    """)


    # 5. Save changes
    connection.commit()


    # 6. Close resources
    cursor.close()
    connection.close()


    print("pets, rooms, and bookings tables created successfully!")


if __name__ == "__main__":
    create_tables()
