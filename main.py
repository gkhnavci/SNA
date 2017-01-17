from py2neo import *

remote_graph = Graph(host="localhost", user="neo4j", password="123456") #connect to db
print("######")
print("Connection Established")
print("######")
print("######")
print("Finding 20 pairs of people where first person is appreciated by second people")
print("######")
for record in remote_graph.data("MATCH (e:Employee)-[:TAKDIR_ALDI]->(t:Takdir)<-[:TAKDIR_ETTI]-(e2:Employee) return e.name,e2.name limit 20"): #run cypher query to get 20 pairs of people about appreciation relation
    print (record['e2.name']+' appreciated '+record['e.name'])  #print proper way
print("######")
print("Listing top 10 admired people")
print("######")
#count TAKDIR_ALDI edges coming into node
#highest degree means highest number of TAKDIR received.
for index,record in enumerate(remote_graph.data("MATCH (e:Employee) - [:TAKDIR_ALDI] -> (Takdir) return e.name,count(Takdir) as degree order by degree desc limit 10 ")):
    print(str(index+1) +' '+record['e.name']+' is '+str(record['degree'])+' times appreciated')
#same logic like above.
#Who admires most can be valuable for people who wants to be appreciated.
print("######")
print("Listing top 10 people who tend to appreciate most")
print("######")
for index,record in enumerate(remote_graph.data("MATCH (e:Employee) - [:TAKDIR_ALDI] -> (Takdir) return e.name,count(Takdir) as degree order by degree desc limit 10 ")):
    print(str(index + 1) + ' ' + record['e.name'] +' ' + str(record['degree']) + ' times appreciated')

#print("Create new type of edge named ROLE_T")
#remote_graph.data("MATCH (e:Employee)-[:TAKDIR_ALDI]->(Takdir)<-[:TAKDIR_ETTI]-(e2:Employee) create (e2)-[r:ROLE_T]->(e) RETURN r")
#these code is commented out because it should be run once
#Here i created new type of edge
#New relationship type which combines both TAKDIR_ALDI & TAKDIR_ETTI
print("######")
print("ROLE_T is a new relation")
print("######")
print("######")
print ("Finding 20 pairs of people where first person  appreciated  second people")
print("######")
for record in remote_graph.data("MATCH (e:Employee)-[:ROLE_T]->(e2:Employee)return e.name,e2.name limit 20"):
    print (record['e.name'] + ' appreciated ' + record['e2.name'])
#Print same thing i did at the beginning
#To test new relationship works fine
print("######")
print("As it is seen this relation is come from collaborative filtering")
print("######")
#New role works fine
print("######")
print ("Checking whether two person appreciated each other or not")
print("######")
#Some people couple may like each other
#Determine these kind of relationships which are rare
#There are some cases such as it can be fake admirations or it can be really good coworkers.
for record in remote_graph.data("MATCH (e:Employee)-[:ROLE_T]->(e2:Employee) where (e2)-[:ROLE_T]->(e) return e.name,e2.name "):
    print(record['e.name']+' and '+record['e2.name']+' appreciated each other')
print("######")
print ("Calculating Degree Centrality...")
print("######")
#Highest degree centrality can indicate more important nodes.
#Here all degree centrality for each node is calculated and first 10 are listed below
for index,record in enumerate(remote_graph.data("MATCH (e:Employee)-[t:ROLE_T]->(e2:Employee) return e.name,count(t) as degreeScore order by degreeScore desc limit 15")):
    print(str(index + 1)+' '+record['e.name']+' has '+str(record['degreeScore'])+' degree centrality')
print("######")
print ("Calculating Betweenness Centrality...")
print("######")
#Another metric for calculating centrality
#Calculate centrality by considering number of occurance in every each shortest path
for index,record in enumerate(remote_graph.data("MATCH p=allShortestPaths((e:Employee)-[:ROLE_T*0..3]->(e2:Employee)) WHERE id(e)<id(e2)and length(p)>1 unwind nodes(p)[1..-1]as n return n.name,count(*) as betweenness order by betweenness desc limit 15 ")):
    print(str(index+1)+' '+record['n.name']+' has'+str(record['betweenness'])+' betweenness centrality')
#Degree centrality and Betweenness centrality points out similar and consistent results
print("######")
print("Finding Missing Triads...")
print("######")
#This give me pairs that recommended not directly, recommendation of recommended people exists.
# So that e recommended e2 indirectly some e3 is recommended by e and this e3 recommends e2 meaning that e supports e2 indirectly.
for record in remote_graph.data("match path1=(e:Employee)-[ROLE_T*2..2]-(e2:Employee)where not ((e)-[:ROLE_T]-(e2)) return e.name,e2.name limit 50"):
    print(record['e.name']+','+record['e2.name'])
#code below is commented out because it must be runned once.
#I already run this line so i commented out.
#Below i added new attribute to hold page rank value.
#print("Add new attribute to node")
#remote_graph.data("MATCH (e:Employee) set e+= {rank: 0}")
print("######")
print("rank attribute is added to each Employee node")
print("######")
print("######")
print("Calculating Page Rank...")
print("######")
remote_graph.data("UNWIND range(1,2) AS ROUND MATCH (e:Employee) where rand()<0.1 MATCH (e:Employee)-[:ROLE_T*..10]->(e2:Employee) set e2.rank=coalesce(e2.rank,0)+1;")
print("######")
print ("Print top 10 Employee with highest page rank ")
print("######")
for index,record in enumerate(remote_graph.data("match(e:Employee) return e.name,e.rank order by e.rank desc limit 10")):
    print (str(index+1)+' '+record['e.name']+' has '+str(record['e.rank'])+' page rank')
