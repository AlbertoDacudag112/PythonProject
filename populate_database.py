"""
populate_database.py
Populate RoadEyeDB with diverse test data including users, vehicles, and violations
across different months for chart visualization
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

class DatabasePopulator:
    def __init__(self, host='localhost', database='RoadEyeDB', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("✅ Connected to database")
                return True
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return False
        return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Database connection closed")
    
    def get_next_id(self, table, id_column, prefix):
        """Get next available ID for a table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {id_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                last_num = int(result[0][len(prefix):])
                return f"{prefix}{str(last_num + 1).zfill(3)}"
            else:
                return f"{prefix}001"
        except:
            return f"{prefix}001"
    
    def get_violation_types(self):
        """Get all available violation types"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT ViolationTypeID, ViolationName, FineAmount FROM violation_types")
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"❌ Error getting violation types: {e}")
            return []
    
    def create_users_and_residents(self, count=30):
        """Create multiple users with resident data"""
        print(f"\n📝 Creating {count} users and residents...")
        
        first_names = [
            "Juan", "Maria", "Jose", "Ana", "Pedro", "Rosa", "Carlos", "Elena", "Luis", "Carmen",
            "Miguel", "Sofia", "Antonio", "Isabel", "Ramon", "Teresa", "Fernando", "Patricia",
            "Roberto", "Luz", "Ricardo", "Gloria", "Manuel", "Angela", "David", "Monica",
            "Gabriel", "Diana", "Rafael", "Cristina", "Jorge", "Beatriz", "Alberto", "Sandra",
            "Francisco", "Laura", "Enrique", "Melissa", "Daniel", "Vanessa"
        ]
        
        last_names = [
            "Santos", "Reyes", "Cruz", "Garcia", "Flores", "Ramos", "Mendoza", "Torres",
            "Rivera", "Gonzales", "Fernandez", "Lopez", "Martinez", "Rodriguez", "Perez",
            "Sanchez", "Ramirez", "Dela Cruz", "Villanueva", "Aquino", "Bautista", "Castro",
            "Santiago", "Navarro", "Morales", "Jimenez", "Valdez", "Diaz", "Aguilar", "Romero"
        ]
        
        sex_options = ["Male", "Female"]
        
        addresses = [
            "Purok 1, Barangay San Miguel",
            "Purok 2, Barangay Poblacion",
            "Purok 3, Barangay Matina",
            "Purok 4, Barangay Buhangin",
            "Purok 5, Barangay Talomo",
            "Purok 6, Barangay Agdao",
            "Purok 7, Barangay Panacan",
            "Purok 8, Barangay Sasa",
            "Phase 1, Subdivision A",
            "Phase 2, Subdivision B",
            "Block 3, Lot 5, Village Heights",
            "Block 4, Lot 8, Green Valley",
            "Unit 12, Building A",
            "Unit 15, Building B",
        ]
        
        created_residents = []
        
        try:
            cursor = self.connection.cursor()
            
            for i in range(count):
                # Generate IDs
                user_id = self.get_next_id('users', 'UserID', 'U')
                resident_id = self.get_next_id('residents', 'ResidentID', 'R')
                
                # Generate user data
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}"
                password = "pass123"  # Simple password for testing
                sex = random.choice(sex_options)
                contact = f"09{random.randint(100000000, 999999999)}"
                address = random.choice(addresses)
                
                # Insert user
                user_query = """
                    INSERT INTO users (UserID, Username, Password, UserType, IsActive)
                    VALUES (%s, %s, %s, 'Resident', TRUE)
                """
                cursor.execute(user_query, (user_id, username, password))
                
                # Insert resident
                resident_query = """
                    INSERT INTO residents (ResidentID, UserID, RFirstName, RMiddleName, RLastName, 
                                         Sex, ContactNo, Address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                middle_name = random.choice(["", "M.", "S.", "L.", "A.", "B."])
                cursor.execute(resident_query, (resident_id, user_id, first_name, middle_name,
                                              last_name, sex, contact, address))
                
                created_residents.append({
                    'resident_id': resident_id,
                    'name': f"{first_name} {last_name}"
                })
                
                if (i + 1) % 10 == 0:
                    print(f"  ✓ Created {i + 1} users...")
            
            self.connection.commit()
            cursor.close()
            print(f"✅ Successfully created {count} users and residents")
            return created_residents
            
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error creating users: {e}")
            return []
    
    def create_vehicles(self, residents):
        """Create 1-3 vehicles for each resident"""
        print(f"\n🚗 Creating vehicles for {len(residents)} residents...")
        
        brands = ["Toyota", "Honda", "Mitsubishi", "Nissan", "Suzuki", "Hyundai", "Ford", 
                 "Mazda", "Isuzu", "Kia"]
        
        models = {
            "Toyota": ["Vios", "Innova", "Fortuner", "Wigo", "Rush", "Hilux"],
            "Honda": ["City", "Civic", "CR-V", "BR-V", "Jazz", "Accord"],
            "Mitsubishi": ["Mirage", "Montero", "Adventure", "L300", "Xpander"],
            "Nissan": ["Navara", "Terra", "Almera", "Patrol", "Urvan"],
            "Suzuki": ["Swift", "Dzire", "Ertiga", "Celerio", "Vitara"],
            "Hyundai": ["Accent", "Tucson", "Kona", "Starex", "Reina"],
            "Ford": ["Ranger", "Everest", "EcoSport", "Explorer", "Expedition"],
            "Mazda": ["2", "3", "CX-5", "CX-9", "6"],
            "Isuzu": ["D-Max", "mu-X", "Traviz", "Crosswind"],
            "Kia": ["Picanto", "Soluto", "Sportage", "Carnival", "Sorento"]
        }
        
        colors = ["White", "Black", "Silver", "Red", "Blue", "Gray", "Brown", "Green"]
        
        created_vehicles = []
        
        try:
            cursor = self.connection.cursor()
            
            for resident in residents:
                # Each resident gets 1-3 vehicles
                num_vehicles = random.randint(1, 3)
                
                for _ in range(num_vehicles):
                    vehicle_id = self.get_next_id('vehicles', 'VehicleID', 'VH')
                    
                    # Generate unique plate number
                    plate_no = f"{random.choice(['ABC', 'XYZ', 'DEF', 'GHI', 'JKL'])}" \
                              f"{random.randint(1000, 9999)}"
                    
                    # Check if plate already exists
                    cursor.execute("SELECT VehicleID FROM vehicles WHERE PlateNo = %s", (plate_no,))
                    if cursor.fetchone():
                        plate_no = f"{random.choice(['MNO', 'PQR', 'STU', 'VWX'])}" \
                                  f"{random.randint(1000, 9999)}"
                    
                    brand = random.choice(brands)
                    model = random.choice(models[brand])
                    color = random.choice(colors)
                    
                    query = """
                        INSERT INTO vehicles (VehicleID, ResidentID, PlateNo, Brand, Model, Color)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (vehicle_id, resident['resident_id'], plate_no,
                                         brand, model, color))
                    
                    created_vehicles.append({
                        'vehicle_id': vehicle_id,
                        'resident_id': resident['resident_id'],
                        'plate_no': plate_no
                    })
            
            self.connection.commit()
            cursor.close()
            print(f"✅ Successfully created {len(created_vehicles)} vehicles")
            return created_vehicles
            
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error creating vehicles: {e}")
            return []
    
    def create_violations(self, vehicles, violation_types):
        """Create violations spread across different months"""
        print(f"\n⚠️  Creating violations across different months...")
        
        if not violation_types:
            print("❌ No violation types found")
            return []
        
        created_violations = []
        
        try:
            cursor = self.connection.cursor()
            
            # Define date range (last 12 months)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            # Each vehicle gets 0-5 violations randomly distributed
            for vehicle in vehicles:
                num_violations = random.randint(0, 5)
                
                for _ in range(num_violations):
                    violation_id = self.get_next_id('violations', 'ViolationID', 'V')
                    
                    # Random date within the last 12 months
                    random_days = random.randint(0, 365)
                    violation_date = start_date + timedelta(days=random_days)
                    violation_date_str = violation_date.strftime('%Y-%m-%d')
                    
                    # Random violation type
                    violation_type = random.choice(violation_types)
                    
                    query = """
                        INSERT INTO violations (ViolationID, VehicleID, ViolationTypeID, 
                                              ViolationDate, IsDeleted)
                        VALUES (%s, %s, %s, %s, 0)
                    """
                    cursor.execute(query, (violation_id, vehicle['vehicle_id'],
                                         violation_type['ViolationTypeID'], violation_date_str))
                    
                    created_violations.append({
                        'violation_id': violation_id,
                        'vehicle_id': vehicle['vehicle_id'],
                        'date': violation_date_str,
                        'type': violation_type['ViolationName'],
                        'amount': violation_type['FineAmount']
                    })
            
            self.connection.commit()
            cursor.close()
            print(f"✅ Successfully created {len(created_violations)} violations")
            return created_violations
            
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error creating violations: {e}")
            return []
    
    def create_payments(self, violations):
        """Create payments for some violations (60-80% paid)"""
        print(f"\n💰 Creating payments for violations...")
        
        payment_types = ["Cash", "GCash", "Bank Transfer", "Online"]
        
        try:
            cursor = self.connection.cursor()
            
            # Randomly pay 60-80% of violations
            violations_to_pay = random.sample(violations, 
                                             int(len(violations) * random.uniform(0.6, 0.8)))
            
            for violation in violations_to_pay:
                payment_id = self.get_next_id('payments', 'PaymentID', 'P')
                
                # Generate receipt number
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                random_suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
                receipt_no = f"RCPT-{timestamp}-{random_suffix}"
                
                payment_type = random.choice(payment_types)
                
                # Payment date is 1-30 days after violation date
                violation_date = datetime.strptime(violation['date'], '%Y-%m-%d')
                payment_date = violation_date + timedelta(days=random.randint(1, 30))
                payment_date_str = payment_date.strftime('%Y-%m-%d')
                
                query = """
                    INSERT INTO payments (PaymentID, ViolationID, PaymentType, ReceiptNo,
                                        AmountPaid, PaymentDate, Status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'PAID')
                """
                cursor.execute(query, (payment_id, violation['violation_id'], payment_type,
                                     receipt_no, violation['amount'], payment_date_str))
            
            self.connection.commit()
            cursor.close()
            print(f"✅ Successfully created {len(violations_to_pay)} payments")
            return len(violations_to_pay)
            
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error creating payments: {e}")
            return 0
    
    def show_statistics(self):
        """Display database statistics"""
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        
        try:
            cursor = self.connection.cursor()
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM users WHERE UserType = 'Resident'")
            user_count = cursor.fetchone()[0]
            print(f"👥 Total Residents: {user_count}")
            
            # Count vehicles
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            vehicle_count = cursor.fetchone()[0]
            print(f"🚗 Total Vehicles: {vehicle_count}")
            
            # Count violations
            cursor.execute("SELECT COUNT(*) FROM violations WHERE IsDeleted = 0")
            violation_count = cursor.fetchone()[0]
            print(f"⚠️  Total Violations: {violation_count}")
            
            # Count payments
            cursor.execute("SELECT COUNT(*) FROM payments WHERE Status = 'PAID'")
            payment_count = cursor.fetchone()[0]
            print(f"💰 Total Payments: {payment_count}")
            
            # Monthly breakdown
            cursor.execute("""
                SELECT DATE_FORMAT(ViolationDate, '%Y-%m') as month, COUNT(*) as count
                FROM violations
                WHERE IsDeleted = 0
                  AND ViolationDate >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(ViolationDate, '%Y-%m')
                ORDER BY month
            """)
            monthly = cursor.fetchall()
            
            print("\n📅 Violations by Month (Last 12 months):")
            for month, count in monthly:
                print(f"   {month}: {count} violations")
            
            cursor.close()
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
    
    def populate_all(self, num_users=30):
        """Main method to populate entire database"""
        print("\n" + "="*60)
        print("🚀 STARTING DATABASE POPULATION")
        print("="*60)
        
        if not self.connect():
            return False
        
        try:
            # Get violation types
            violation_types = self.get_violation_types()
            if not violation_types:
                print("⚠️  Warning: No violation types found. Please add violation types first.")
                return False
            
            print(f"✓ Found {len(violation_types)} violation types")
            
            # Create users and residents
            residents = self.create_users_and_residents(num_users)
            if not residents:
                return False
            
            # Create vehicles
            vehicles = self.create_vehicles(residents)
            if not vehicles:
                return False
            
            # Create violations
            violations = self.create_violations(vehicles, violation_types)
            
            # Create payments
            if violations:
                self.create_payments(violations)
            
            # Show statistics
            self.show_statistics()
            
            print("\n✅ DATABASE POPULATION COMPLETED SUCCESSFULLY!")
            return True
            
        except Exception as e:
            print(f"\n❌ Error during population: {e}")
            return False
        finally:
            self.disconnect()


def main():
    """Main execution function"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         RoadEyeDB - Database Population Script            ║
║      Populate database with test data for charting        ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get user input
    try:
        num_users = int(input("Enter number of users to create (default 30): ") or "30")
    except ValueError:
        num_users = 30
        print(f"Using default: {num_users} users")
    
    # Database configuration
    print("\n📋 Database Configuration:")
    host = input("Host (default: localhost): ") or "localhost"
    database = input("Database name (default: RoadEyeDB): ") or "RoadEyeDB"
    user = input("Username (default: root): ") or "root"
    password = input("Password (default: empty): ") or ""
    
    # Confirm
    print(f"\n⚠️  This will add {num_users} users with vehicles and violations to {database}")
    confirm = input("Continue? (y/n): ").lower()
    
    if confirm != 'y':
        print("❌ Operation cancelled")
        return
    
    # Execute population
    populator = DatabasePopulator(host, database, user, password)
    populator.populate_all(num_users)


if __name__ == "__main__":
    main()
