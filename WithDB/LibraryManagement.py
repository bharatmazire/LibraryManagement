import pymysql as pms
import getpass as gp
import datetime as dt

def craete_connection(name , passwd , table):
	db = pms.connect("localhost" , name , passwd , table)
	crsr = db.cursor()
	return db, crsr
	
def close_connection(db):
	db.close()
		
		
def show_books(crsr):			# we can add one more parameter like which function is calling , so that accoringly we can chang output format 
	print ("\n\t\t\t\tShowing Book List \n\n ")
	sql = "select id , book_name , author_name from LibraryBooks"
	crsr.execute(sql)
	result = crsr.fetchall()
	for row in result:
		print ("Book ID : {} \nBook name : {} \nAuthor name : {}\n\n".format(row[0],row[1],row[2]))

def search(crsr , column_name , value):
	sql = "select id , book_name , author_name from LibraryBooks where {} = {}".format(column_name , value)
			if crsr.execute(sql) == 1:
				result = crsr.fetchall()
				for row in result:
					print ("Book ID : {} \nBook name : {} \nAuthor name : {}\n\n".format(row[0],row[1],row[2]))
			else:
				print ("No result found !!")


def search_books(crsr):
	print ("\n\t\t\t\tSearching Books in Book List \n\n ")
	ch = 0
	while ch != 4:
		ch = int(input("Search by \n1.Book Name \n2.Author Name \n3.Show All \n4.Exit \nYour choice : "))
		if ch == 1:
			book_name = str(input("Enter Book name : "))
			search(crsr , 'book_name' , book_name)
		
		elif ch == 2:
			author_name = str(input("Enter Author name : "))
			search(crsr , 'author_name' , author_name)
					
		elif ch == 3:
			show_books(crsr)
		
		elif ch == 4:
			print ("Exiting from Search Book !! \nB Y E")
		
		else:
			print ("Wrong chioce ")
			

def main():
	connection_name = "root" 		#str(input("Enter login name : "))
	conncetion_password = "root" 	#str(gp.getpass("Enter login password : "))
	table_name = "library" 			#str(input("Table name : "))

	db , crsr = craete_connection(connection_name , conncetion_password , table_name)
	
	choice = 1
	while choice != 6:
		choice = int(input("1.Show Books \n2.Search Book \n3.Give Book \n4.Submit Book \n5.Add Book \n6.Remove Book \n7.Exit \n Your Choice : "))
		
		if choice == 1:
			show_books(crsr)
		
		elif choice == 2:
			search_books(crsr)
			
		elif choice == 3:
			print ("Give Book")
			print ("You must know the BOOK ID for getting book ")
			while ch != 3:
				ch = int(input("1. show books 2. search books 3.I know book id so exit \nChoice : "))
				if ch == 1:
					show_books(crsr)
				elif ch == 2:
					search_books(crsr)
				elif ch == 3:
					pass
				else:
					print "Wrong Choice "
			
			ID = int(input("Enter ID of BOOK : "))
			sql = "select book_issued_person_name from LibraryBooks where id = {}".format(ID)
			
			if crsr.execute(sql) == 1:
				result = crsr.fetch()
				if result != '':
					today_date = str(dt.datetime.now())[0:10]
					name = str(input("Enter name : "))
					sql = "update LibraryBooks SET book_issued_person_name = '{}',book_issued_date = '{}' where id = {}".format(name,today_date,ID)
					crsr.exexute(sql)
				else:
					print ("Book Already taken by {}".format(result))
			else:
				print ("No result found !!")
			
		elif choice == 4:
			print ("You must know the BOOK ID for getting book ")
			while ch != 3:
				ch = int(input("1. show books 2. search books 3.I know book id so exit \nChoice : "))
				if ch == 1:
					show_books(crsr)
				elif ch == 2:
					search_books(crsr)
				elif ch == 3:
					pass
				else:
					print "Wrong Choice "
			
			ID = int(input("Enter ID of BOOK : "))
			name = str(input("Enter name : "))
			sql = "select book_issued_person_name from LibraryBooks where id = {}".format(ID)
			if crsr.execute(sql) == 1:
				result = crsr.fetch()
				if result == name:
					sql = "update LibraryBooks SET book_issued_person_name = '{}',book_issued_date = '{}' where id = {}".format('','',ID)
					crsr.exexute(sql)
				else:
					print ("Wrong book !!")
			else:
				print ("not found")
			
		elif choice == 5:
			print ("\n\t\t\t\tAdding Book in List \n\n ")
			
			count = int(input("How many books you want to add ? "))
			
			while count != 0:
				book_name = str(input("Enter Book Name : "))[0:250]
				author_name = str(input("Enter Author Name : "))[0:250]
				today_date = str(dt.datetime.now())[0:10]
				sql = "insert into LibraryBooks (book_name,author_name,added_date) values ('{}','{}','{}')".format(book_name,author_name,today_date)
				
				if crsr.execute(sql) == 1:
					print ("Book : {} Added !".format(book_name))
					db.commit()
				else:
					print ("Book : {}  Not added !".format(book_name))
					db.rollback()
					if count != 1:
						print ("Try Next Book !!")
				
				count = count - 1

		elif choice == 6:
			print ("\n\t\t\t\tRemoving Book from List \n\n ")
			print ("\n\t **** YOU CAN REMOVE BOOK BY USING THEIR ID ***** ")
			print ("\n\n PLEASE NOTE DOWN THE #ID OF BOOK YOU WANT TO REMOVE \n\n ")
			
			ch = 0
			while ch != 3:
				ch = int(input("1.show all books 2.search book 3.exit \n your choice : "))
				if ch == 1:
					show_books(crsr)
				elif ch == 2:
					search_books(crsr)
				else:
					print "Wrong choice" # we can add 3 wrong choice ==  exit 
			
			ID = int(input("Enter Book Id you want to remove : "))
			sql = "delete from LibraryBooks where id == {}".format(ID)
			
			if crsr.execute(sql) == 1:
				print ("Book removed")
				db.commit()
			else:
				print ("Book not removed")
				db.rollback()
				
		elif choice == 7:
			print ("HAVE A NICE DAY \n B Y E")
			
		else:							# we can add 3 wrong choice ==  exit 
			print ("Wrong choice !!!")

	close_connection(db) 

if __name__ == '__main__':
	main()
