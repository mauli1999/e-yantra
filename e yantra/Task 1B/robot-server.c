/*
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
*/

/*
* Team ID:		[ 3523 ]
* Author List:		[ Harsh Thakur ]
* Filename:		robot-server.c
* Functions:		[ receive_from_send_to_client, socket_create ]
* 					[ Comma separated list of functions in this file ]
* Global variables:	[ SERVER_PORT, RX_BUFFER_SIZE, TX_BUFFER_SIZE, ERROR, MAXCHAR, dest_addr, source_addr, rx_buffer, tx_buffer, ipv4_addr_str[128], ipv4_addr_str_client[128], listen_sock, line_data, i, flag, flag_reset, count, in_line, input_fp, output_fp]
* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024
#define ERROR -1

#define MAXCHAR 1000			// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];		// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;			// socket for server

char line_data[MAXCHAR];		// buffer to store data from file that needs to be send to client
int i=3;				// this is used for sending particular data
int flag=1;				// Flag to send an $ to the client
int flag_reset=0;			// Flag to make again to 1
int count=0;				// Count to go a particular line in the obstacle
int in_line;				// in_line is the first letter of the line

FILE *input_fp, *output_fp;


/*
* Function Name:	socket_create
* Inputs:		dest_addr [ structure type for destination address ]
* 				source_addr [ structure type for source address ]
* Outputs: 		my_sock [ socket value, if connection is properly created ]
* Purpose: 		the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr)
{
	int addr_family;
	int ip_protocol;
	int sockaddr_len = sizeof(struct sockaddr_in); // Added
	// listen_sock is for server
	// int listen_sock global variavble
	
	// my_sock is for client
	int my_sock;
	
	
	if( (listen_sock = socket( AF_INET, SOCK_STREAM, 0 ) ) == ERROR )
	{
		perror("Socket :- ");
		exit(-1);
	}

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;
	bzero(&dest_addr.sin_zero, 8);
		
	if( ( bind( listen_sock, ( struct sockaddr * )&dest_addr, sockaddr_len ) ) == ERROR )
	{
		perror("Bind :- ");
		exit(-1);	
	}
	
	
	strcpy( ipv4_addr_str, inet_ntoa( dest_addr.sin_addr ) );
	
	printf("[DEBUG] Self IP = %s\n", ipv4_addr_str);
	printf("[DEBUG] Socket created\n");
	printf("[DEBUG] Socket bound, port %d\n", ntohs( dest_addr.sin_port ) );
	
	if( ( listen( listen_sock, 1 ) ) == -1 )
	{		
		perror("Listern :- ");
		exit(-1);
	}
	
	printf("[DEBUG] Socket listening\n");
	
	if( ( my_sock = accept( listen_sock, ( struct sockaddr * )&source_addr, &sockaddr_len ) ) == ERROR )
	{
		perror("Accept :- ");
		exit(-1);
	}
	
	strcpy( ipv4_addr_str_client, inet_ntoa( source_addr.sin_addr ) );
	// printf("New Client Connected from port no %d and IP %s\n", ntohs( source_addr.sin_port ), ipv4_addr_str_client);
	
	printf("[DEBUG] Socket accepted\n");

	return my_sock;
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:		sock [ socket value, if connection is properly created ]
* Outputs: 		None
* Purpose: 		the function receives the data from server and updates the 'rx_buffer'
*				variable with it, sends the obstacle position based on obstacle_pos.txt
*				file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock)
{
	// Here in this particular Funtion sock means client
	// To store data from client
	// We have char rx_buffer[RX_BUFFER_SIZE] global variable
	
	// To store data that need to be send to client
	// We have char tx_buffer[RX_BUFFER_SIZE] global variable
		
	// Data length to store length of data
	int data_len;
	printf("\n");
	printf("______________________________________________\n");
	
	// Let us find the data length first to print it
	data_len = 1;
	data_len = recv(sock, rx_buffer, 1024, 0);
	printf("[DEBUG] Received %d bytes from %s:\n", data_len, ipv4_addr_str);
	printf("[DEBUG] Data Received = ");
		
	if( data_len )
	{
		rx_buffer[data_len] = '\0';
		printf("%s", rx_buffer);
	}
	
	printf("\n");
	// printf("Line data:-\n");
	// printf("**%s**\n", line_data);
	int length_da = strlen(line_data);
	// printf("Length = %d\n", length_da);
	// printf("I = %d\n", i);
	
	// printf("Line to be read from the obstacle:- %c\n", rx_buffer[0]);
	count = rx_buffer[0] - '0';		// count is the first letter if the received file
	// printf("count = %d\n", count);
	
	in_line = line_data[0] - '0';		// in_line is the first letter 
	// printf("in_line = %d\n", in_line);
	
	while( count != in_line )
	{
		flag = 1;
		fgets(line_data, MAXCHAR, input_fp);
		
		// printf("\n");
		// printf("Line data:-\n");
		// printf("**%s**\n", line_data);
		int length_da = strlen(line_data);
		// printf("Length = %d\n", length_da);
		// printf("I = %d\n", i);
		
		in_line = line_data[0] - '0';		// in_line is the first letter 
		// printf("in_line = %d\n", in_line);
		
		if( in_line > count)
		{
			flag = 0;	
			break;		
		}
	}
	
	
	
	
	// Empty string in the begning at first
	strcpy(tx_buffer, "");
	char check;
	check = ' ';
	
	// Goes in "IF" condition if there obstacles
	if(flag == 1)
	{
		// append ch to str 
		strcat(tx_buffer, "@");
		
		check = line_data[i];
		// printf("%c", check);
		strncat(tx_buffer, &check, 1);
		i = i + 1;
		
		while( check != ')')
		{
			check = line_data[i];
			// printf("%c", check);
			strncat(tx_buffer, &check, 1);
			i = i + 1;
		}
		
		strcat(tx_buffer, "@");
		
		check = line_data[i];
		// printf("%c", check);
		i = i + 2;
		flag_reset = 0;
	}
	// Goes in "ELSE" if there are no obstacles
	else if(flag == 0)
	{
		strcat(tx_buffer, "@");
		strcat(tx_buffer, "$");
		strcat(tx_buffer, "@");
		flag_reset = 1;
		i = 3;
	}
	// printf("\n");
	if( check != ';' )
	{
		if( flag_reset == 1 )
			flag = 1;
		else
			flag = 0;
	}
	else
	{
		flag = 1;
	}
	 
	// Now send data to the client
	send( sock, tx_buffer, strlen( tx_buffer ), 0 );
	
	// Print the required data
	printf("[DEBUG] Transmitted %ld bytes: %s\n", strlen( tx_buffer ), tx_buffer);
	
	return 0;
}


int main()
{
	char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL)
	{
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if(output_fp == NULL)
	{
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1)
	{
		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);

		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);

	}

	return 0;
}

