
from functools import partial
import numpy as np


import easysparql
import data_extraction
import learning

from models import MLModel

QUERY_LIMIT = "LIMIT 100"


# def explore_and_train(endpoint=None, model_id=None):
#     if endpoint is None:
#         print "explore_and_train> endpoint is None"
#         return
#     if model_id is None:
#         print "explore_and_train> model_id should not be None"
#         return
#     try:
#         update_model_state(model_id=model_id, new_state=MLModel.RUNNING, new_progress=10,
#                            new_notes="Extracting numerical class/property combinations")
#         # Safe function
#         classes_properties_uris = easysparql.get_all_classes_properties_numerical(endpoint=endpoint)
#         update_model_state(model_id=model_id, new_progress=30,
#                            new_notes="extracted all class/property numerical combinations")
#         data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
#             class_property_uris=classes_properties_uris)
#         update_model_state(model_id=model_id, new_progress=40, new_notes="extracted meta_data")
#         if np.any(np.isnan(data)):
#             print "explore_and_train> there is a nan in the data"
#             print "**************************"
#         else:
#             print "explore_and_train> no nans in the data"
#         # data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
#         model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
#         update_model_state(model_id=model_id, new_progress=60, new_notes="trained the model")
#         meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
#         update_model_state(model_id=model_id, new_progress=70, new_notes="extract clusters from meta")
#         # print "model num_of_clusters: %d" % model.n_clusters
#         # print "cluster centers: %s" % str(model.cluster_centers_)
#         learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)
#         update_model_state(model_id=model_id, new_progress=90, new_notes="Saving the model data")
#         model_file_name = data_extraction.save_model(model=model, file_name=model_id + "-")
#         if model_file_name is not None:
#             m = MLModel.objects.filter(id=model_id)
#             if len(m) == 1:
#                 m.file_name = model_file_name
#                 m.save()
#                 update_model_state(model_id=model_id, new_progress=100, new_notes="Completed")
#             else:
#                 update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="model is deleted")
#         else:
#             update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Error Saving the model")
#     except Exception as e:
#         print "explore_and_train> Exception %s" % str(e)
#         update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Not captured error: " + str(e))


def explore_and_train(endpoint=None, model_id=None):
    if endpoint is None:
        print "explore_and_train> endpoint is None"
        return
    if model_id is None:
        print "explore_and_train> model_id should not be None"
        return
    try:
        update_progress_func = partial(update_model_progress_for_partial, model_id)
        update_model_state(model_id=model_id, new_state=MLModel.RUNNING,
                           new_notes="Extracting numerical class/property combinations")
        # Safe function
        classes_properties_uris = easysparql.get_all_classes_properties_numerical(endpoint=endpoint)
        update_model_state(model_id=model_id,
                           new_notes="extracting values from gathered class/property")
        data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
            class_property_uris=classes_properties_uris, update_func=update_progress_func)
        update_model_state(model_id=model_id, new_notes="extracted meta_data")
        if np.any(np.isnan(data)):
            print "explore_and_train> there is a nan in the data"
            print "**************************"
        else:
            print "explore_and_train> no nans in the data"
        # data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
        model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
        update_model_state(model_id=model_id,  new_notes="trained the model")
        meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
        update_model_state(model_id=model_id,  new_notes="extract clusters from meta")
        # print "model num_of_clusters: %d" % model.n_clusters
        # print "cluster centers: %s" % str(model.cluster_centers_)
        learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)
        update_model_state(model_id=model_id, new_notes="Saving the model data")
        model_file_name = data_extraction.save_model(model=model, file_name=str(model_id)+" - ")
        if model_file_name is not None:
            m = MLModel.objects.filter(id=model_id)
            if len(m) == 1:
                m.file_name = model_file_name
                m.save()
                update_model_state(model_id=model_id, new_notes="Completed")
            else:
                update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="model is deleted")
        else:
            update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Error Saving the model")
    except Exception as e:
        print "explore_and_train> Exception %s" % str(e)
        update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Not captured error: " + str(e))


def update_model_progress_for_partial(model_id, new_prgress):
    return update_model_state(model_id=model_id, new_progress=new_prgress)

# def test_progress(model_id=None):
#     if model_id is None:
#         print "test_progress> model id is None"
#         return


def update_model_state(model_id=None, new_state=None, new_notes=None, new_progress=None):
    m = MLModel.objects.filter(id=model_id)
    if len(m) != 0:
        m = m[0]
        if new_state is not None:
            m.state = new_state
        if new_notes is not None:
            m.notes = new_notes
        if new_progress is not None:
            m.progress = new_progress
        m.save()
        return m
    return None
