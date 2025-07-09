import io
import os
import schedule
import threading
import time
import uuid
from datetime import datetime, timedelta
import kubernetes
import yaml
from dotenv import load_dotenv, find_dotenv
from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   request,
                   session)
from flask_bootstrap import Bootstrap5
from secret_key_generator import secret_key_generator

from forms import (CreateCodeGenForm,
                   QuestionForm,
                   ReviewForm,
                   ExplainForm,
                   K8sClusterForm,
                   K8sNamespaceForm,
                   K8sPodsForm,
                   ScanK8sDeploySts)
from k8scluster import K8sCluster

from src.kube_debugger_crew.crew import KubeDebuggerCrew
from src.kube_chatter_crew.crew import KubeChatterCrew
from src.kube_reviewer_crew.crew import KubeReviewerCrew
from src.kube_security_crew.crew import KubeSecurityCrew
from src.kube_developer_crew.crew import KubeDeveloperCrew
from src.kube_explainer_crew.crew import KubeExplainerCrew

app = Flask(__name__)
# Generate an SHH key
app.config['SECRET_KEY'] = secret_key_generator.generate(len_of_secret_key=32)
Bootstrap5(app)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Create the uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

cleanup_lock = threading.Lock()
# Load the environment variables to connect to watsonx and serper
if load_dotenv(find_dotenv()):
    # Env variables exist in .env file, use them. Else these env variables must be set
    os.environ["MISTRAL_MODEL"] = os.getenv("MISTRAL_MODEL")
    os.environ["GRANITE_MODEL"] = os.getenv("GRANITE_MODEL")
    os.environ["WX_API_KEY"] = os.getenv("WX_API_KEY")
    os.environ["WX_URL"] = os.getenv("WX_URL")
    os.environ["WX_PROJECT_ID"] = os.getenv("WX_PROJECT_ID")
    os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
    os.environ["TEAM_NAME"] = os.getenv("TEAM_NAME")
    os.environ["CONTACT_EMAILS"] = os.getenv("CONTACT_EMAILS")
else:
    # Only hardcode model names. Others env variables should be injected
    os.environ["MISTRAL_MODEL"] = "watsonx_text/mistralai/mistral-large"
    os.environ["GRANITE_MODEL"] = "watsonx_text/ibm/granite-3-8b-instruct"

team_name = os.environ.get('TEAM_NAME')
contact_emails = os.environ.get('CONTACT_EMAILS')


def periodic_cleanup():
    """Function to clean up files older than a certain time."""
    with cleanup_lock:
        current_time = datetime.now()
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            age = current_time - modified_time

            # Define the time threshold for file deletion (e.g., 1 hour)
            max_age = timedelta(hours=8)

            if age > max_age:
                os.remove(file_path)
                print(f"File {filename} deleted due to age.")


# Schedule the cleanup function to run every minute
schedule.every().minute.do(periodic_cleanup)


# Continuously run the scheduled tasks in a separate thread
def scheduled_task():
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Sleep for 1 second to avoid excessive CPU usage


cleanup_thread = threading.Thread(target=scheduled_task, daemon=True)
cleanup_thread.start()


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html", team_name=team_name)


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html", team_name=team_name, contact_emails=contact_emails)


@app.route("/contact", methods=['GET'])
def contact():
    return render_template("contact.html", team_name=team_name,
                           contact_emails=contact_emails)


@app.route("/generate", methods=['GET', 'POST'])
def generate_code():
    codegen_form = CreateCodeGenForm()
    if codegen_form.validate_on_submit():
       # generate_code = GenerateCode(codegen_form.instruction.data)

        inputs = {
            "instruction": codegen_form.instruction.data,
        }
        codegen_form.result.data = KubeDeveloperCrew().crew().kickoff(inputs=inputs)

    return render_template("generate.html", form=codegen_form, team_name=team_name)


@app.route("/question", methods=['GET', 'POST'])
def question():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
      #  ask_question = AskQuestion(question_form.question.data)

        inputs = {
            "question": question_form.question.data,
        }
        question_form.result.data = KubeChatterCrew().crew().kickoff(inputs=inputs)

    return render_template("question.html", form=question_form, team_name=team_name)


@app.route("/review", methods=['GET', 'POST'])
def review():
    review_form = ReviewForm()
    if review_form.validate_on_submit():
        #review_code = ReviewCode(review_form.code_input.data)

        inputs = {
            "review_content": review_form.code_input.data,
        }
        review_form.result.data = KubeReviewerCrew().crew().kickoff(inputs=inputs)


    return render_template("review.html", form=review_form, team_name=team_name)


@app.route("/explain", methods=['GET', 'POST'])
def explain():
    explain_form = ExplainForm()
    if explain_form.validate_on_submit():
        #explain_code = ExplainCode(explain_form.code_input.data)

        inputs = {
            "explain_code": explain_form.code_input.data,
        }
        explain_form.result.data = KubeExplainerCrew().crew().kickoff(inputs=inputs)

    return render_template("explain.html", form=explain_form, team_name=team_name)


@app.route("/cluster/", methods=['GET', 'POST'])
def connect_cluster():
    k8cluster_form = K8sClusterForm()
    if k8cluster_form.validate_on_submit():
        kubeconfig_file = k8cluster_form.kubeconfig.data
        filename = str(uuid.uuid4()) + '_' + kubeconfig_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        kubeconfig_file.save(file_path)
        # kubeconfig_content = kubeconfig_file.read().decode('utf-8')
        # kubeconfig_file_object = io.BytesIO(kubeconfig_content.encode('utf-8'))
        session['kubeconfig'] = file_path

        # config_data = yaml.safe_load(kubeconfig_content)
        # global current_context
        # current_context = config_data.get('current-context', None)
        # global k8scluster
        # k8scluster = K8sCluster(configfile=kubeconfig_file_object)
        return redirect(url_for('pull_namespaces'))
    return render_template('k8sissue.html', form=k8cluster_form, team_name=team_name)


# Below method added for Kubernetes Cluster security scanning
@app.route("/k8scluster/", methods=['GET', 'POST'])
def connect_k8scluster():
    k8cluster_form = K8sClusterForm()
    if k8cluster_form.validate_on_submit():
        kubeconfig_file = k8cluster_form.kubeconfig.data
        filename = str(uuid.uuid4()) + '_' + kubeconfig_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        kubeconfig_file.save(file_path)
        # kubeconfig_content = kubeconfig_file.read().decode('utf-8')
        # kubeconfig_file_object = io.BytesIO(kubeconfig_content.encode('utf-8'))
        session['kubeconfig'] = file_path

        # config_data = yaml.safe_load(kubeconfig_content)
        # global current_context
        # current_context = config_data.get('current-context', None)
        # global k8scluster
        # k8scluster = K8sCluster(configfile=kubeconfig_file_object)
        return redirect(url_for('pull_k8snamespaces'))
    return render_template('k8ssecurity.html', form=k8cluster_form, team_name=team_name)


@app.route("/cluster/namespaces/", methods=['GET', 'POST'])
def pull_namespaces():
    k8sns_form = K8sNamespaceForm()
    file_path = session.get('kubeconfig')
    if file_path is None:
        flash(f"Error connecting to cluster. Please re-upload valid kubeconfig file")
        return redirect(url_for('connect_cluster'))

    with open(file_path, 'r') as file:
        file_content = file.read()

    kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
    config_data = yaml.safe_load(file_content)
    current_context = config_data.get('current-context', None)
    k8scluster = K8sCluster(configfile=kubeconfig_file_object)

    k8sns_form.cluster_api_url.data = current_context
    try:
        namespaces = k8scluster.list_namespaces()
    except kubernetes.client.exceptions.ApiException:
        flash('Unauthorized exception. Update the Kubeconfig file and retry.')
        return redirect(url_for('connect_cluster'))
    except Exception as e:
        flash(f"Error connecting to cluster: {str(e)}")
        return redirect(url_for('connect_cluster'))
    k8sns_form.namespaces.choices = namespaces
    if k8sns_form.validate_on_submit():
        selected_ns = k8sns_form.namespaces.data
        return redirect(url_for('pull_unhealthy_pods', namespace=selected_ns))
    return render_template('k8sns.html', form=k8sns_form, team_name=team_name)


# Below method added for pulling namespaces for cluster security scan
@app.route("/k8scluster/namespaces/", methods=['GET', 'POST'])
def pull_k8snamespaces():
    k8sns_form = K8sNamespaceForm()
    file_path = session.get('kubeconfig')
    if file_path is None:
        flash(f"Error connecting to cluster. Please re-upload valid kubeconfig file")
        return redirect(url_for('connect_k8scluster'))

    with open(file_path, 'r') as file:
        file_content = file.read()

    kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
    config_data = yaml.safe_load(file_content)
    current_context = config_data.get('current-context', None)
    k8scluster = K8sCluster(configfile=kubeconfig_file_object)

    k8sns_form.cluster_api_url.data = current_context
    try:
        namespaces = k8scluster.list_namespaces()
    except kubernetes.client.exceptions.ApiException:
        flash('Unauthorized exception. Update the Kubeconfig file and retry.')
        return redirect(url_for('connect_k8scluster'))
    except Exception as e:
        flash(f"Error connecting to cluster: {str(e)}")
        return redirect(url_for('connect_k8scluster'))
    k8sns_form.namespaces.choices = namespaces
    if k8sns_form.validate_on_submit():
        selected_ns = k8sns_form.namespaces.data
        return redirect(url_for('pull_deploy_sts', namespace=selected_ns))
    return render_template('k8ssecurityns.html', form=k8sns_form, team_name=team_name)


@app.route("/cluster/namespaces/<namespace>/deploysts", methods=['GET', 'POST'])
def pull_deploy_sts(namespace: str):
    scank8s_form = ScanK8sDeploySts()
    file_path = session.get('kubeconfig')
    if file_path is None:
        flash(f"Error connecting to cluster. Please re-upload valid kubeconfig file")
        return redirect(url_for('connect_k8scluster'))
    with open(file_path, 'r') as file:
        file_content = file.read()
    kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
    config_data = yaml.safe_load(file_content)
    current_context = config_data.get('current-context', None)
    k8scluster = K8sCluster(configfile=kubeconfig_file_object)

    scank8s_form.cluster_api_url.data = current_context
    try:
        scank8s_form.namespaces.choices = k8scluster.list_namespaces()
        deployments = k8scluster.list_deploys(ns=namespace)
        statefulsts = k8scluster.list_sts(ns=namespace)
        list_deploy_sts = []
        for deployment in deployments:
            entity = {
                "name": deployment,
                "kind": "Deployment"
            }
            list_deploy_sts.append(entity)
        for sts in statefulsts:
            entity = {
                "name": sts,
                "kind": "StatefulSet"
            }
            list_deploy_sts.append(entity)
        if len(list_deploy_sts) == 0:
            flash(
                f'No Deployments or Statefulsets found in the namespace: {namespace}. Select another namespace to check.')
            return redirect(url_for('pull_k8snamespaces'))
        scank8s_form.deploysts.choices = list_deploy_sts
    except kubernetes.client.exceptions.ApiException:
        flash('Unauthorized exception. Update the Kubeconfig file and retry.')
        return redirect(url_for('connect_k8scluster'))
    except Exception as e:
        flash(f"Error connecting to cluster: {str(e)}")
        return redirect(url_for('connect_k8scluster'))
    scank8s_form.namespaces.data = namespace

    if scank8s_form.validate_on_submit():
        if request.form.get('submit'):
            selected_ns = namespace
            selected_obj = eval(scank8s_form.deploysts.data)
            if selected_obj['kind'] == "Deployment":
                deploy_name = selected_obj['name']
                deploy_yaml = k8scluster.get_deploy_yaml(ns=selected_ns, deploy_name=deploy_name)

                inputs = {
                    "deploy_sts_yaml": deploy_yaml,
                }
                scank8s_form.result.data = KubeSecurityCrew().crew().kickoff(inputs=inputs)

            elif selected_obj['kind'] == "StatefulSet":
                sts_name = selected_obj['name']
                sts_yaml = k8scluster.get_sts_yaml(ns=selected_ns, sts_name=sts_name)

                inputs = {
                    "deploy_sts_yaml": sts_yaml,
                }
                scank8s_form.result.data = KubeSecurityCrew().crew().kickoff(inputs=inputs)
        elif request.form.get('show_yaml'):
            selected_ns = namespace
            selected_obj = eval(scank8s_form.deploysts.data)
            if selected_obj['kind'] == "Deployment":
                deploy_name = selected_obj['name']
                deploy_yaml = k8scluster.get_deploy_yaml(ns=selected_ns, deploy_name=deploy_name)
                scank8s_form.result.data = deploy_yaml
            elif selected_obj['kind'] == "StatefulSet":
                sts_name = selected_obj['name']
                sts_yaml = k8scluster.get_sts_yaml(ns=selected_ns, sts_name=sts_name)
                scank8s_form.result.data = sts_yaml
    return render_template('k8sscandeploysts.html', form=scank8s_form, team_name=team_name)


@app.route("/cluster/namespaces/<namespace>", methods=['GET', 'POST'])
def pull_unhealthy_pods(namespace: str):
    k8spod_form = K8sPodsForm()
    file_path = session.get('kubeconfig')
    if file_path is None:
        flash(f"Error connecting to cluster. Please re-upload valid kubeconfig file")
        return redirect(url_for('connect_cluster'))
    with open(file_path, 'r') as file:
        file_content = file.read()
    kubeconfig_file_object = io.BytesIO(file_content.encode('utf-8'))
    config_data = yaml.safe_load(file_content)
    current_context = config_data.get('current-context', None)
    k8scluster = K8sCluster(configfile=kubeconfig_file_object)

    k8spod_form.cluster_api_url.data = current_context
    try:
        k8spod_form.namespaces.choices = k8scluster.list_namespaces()
        unhealthy_pods = k8scluster.unhealthy_pods(ns=namespace)
        if len(unhealthy_pods) == 0:
            flash(f'No unhealthy pod found in namespace: {namespace}. Select another namespace to check.')
            return redirect(url_for('pull_namespaces'))
        k8spod_form.pods.choices = unhealthy_pods
    except kubernetes.client.exceptions.ApiException:
        flash('Unauthorized exception. Update the Kubeconfig file and retry.')
        return redirect(url_for('connect_cluster'))
    except Exception as e:
        flash(f"Error connecting to cluster: {str(e)}")
        return redirect(url_for('connect_cluster'))
    k8spod_form.namespaces.data = namespace

    if k8spod_form.validate_on_submit():
        if request.form.get('submit'):
            selected_ns = namespace
            selected_pod = k8spod_form.pods.data

            # Hand over to Crew to diagnose the issue and provide recommendation

            pod_status = k8scluster.pod_status_details(ns=selected_ns, podname=selected_pod)

            inputs = {
                "selected_ns": namespace,
                "selected_pod": k8spod_form.pods.data,
                "issue": pod_status.__str__(),
            }
            k8spod_form.result.data = KubeDebuggerCrew().crew().kickoff(inputs=inputs)

        elif request.form.get('show_yaml'):

            selected_ns = namespace
            selected_pod = k8spod_form.pods.data
            pod_yaml = k8scluster.get_pod_yaml(ns=selected_ns, podname=selected_pod)
            k8spod_form.result.data = pod_yaml
    return render_template('k8spods.html', form=k8spod_form, team_name=team_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
