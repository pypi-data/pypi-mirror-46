import jpype
from jpype import JPackage

jvmPath = jpype.getDefaultJVMPath()
# jpype.startJVM(jvmPath)
# jpype.java.lang.System.out.println("hello world!")
# jpype.java.lang.System.out.println("I hate you!")
#
# jpype.shutdownJVM()
#

#jarPath =  "/Users/junyin/IdeaProjects/SmoothNLP/smoothnlp_maven/target/classes/com/smoothnlp/nlp/SmoothNLP.class"
jarPath =  "/Users/junyin/IdeaProjects/SmoothNLP/smoothnlp_maven/target/smoothnlp-0.2-jar-with-dependencies.jar"
#jarPath =  "/Users/junyin/IdeaProjects/SmoothNLP/smoothnlp_maven/target/smoothnlp-0.2-exec.jar"


jpype.startJVM(jvmPath,
    "-Djava.class.path=%s" % jarPath)

import json
st = JPackage("com.smoothnlp.nlp").SmoothNLP
res = st.postag("国泰君安上季度盈利1千万")
print(res)
print(type(res))
print(json.loads(res))
print(type(res))

res = st.ner("国泰君安上季度盈利1千万")
print(res)
print(type(res))
print(json.loads(res))
print(type(res))


print ('-' * 10)
from smoothnlp.server import smoothNlpRequest

nlp= smoothNlpRequest()

res = nlp.segment("国泰君安上季度盈利1千万")
print(res)
res = nlp.postag("国泰君安上季度盈利1千万")
print(res)
res = nlp.ner("国泰君安上季度盈利1千万")
print(res)



