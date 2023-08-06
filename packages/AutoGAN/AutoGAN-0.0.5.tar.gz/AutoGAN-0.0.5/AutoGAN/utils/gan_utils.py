
def prepare_compile(names=[], losses_in=[], metrics_in=[], loss_weights=[]):
    losses = {}
    metrics = {}
    weights = {}

    for i, name in enumerate(names):
        if len(losses_in) > i:
            losses[name] = losses_in[i]
            metrics[name] = metrics_in[i] if len(metrics_in) > i else []
            weights[name] = loss_weights[i] if len(loss_weights) > i else 1
        else:
            break
    return losses, metrics, weights


def extend(alist, anobject):
    assert isinstance(alist, list), "must provide a list to extend"
    alist.extend(anobject if isinstance(anobject, list) else [anobject])


def get_model_output(model, batch_size=None):
    model_outputs = model.outputs
    if batch_size is None:
        if isinstance(model_outputs, list):
            if len(model_outputs) > 1:
                return [tuple(inputs.get_shape().as_list()) for inputs in model_outputs]
            else:
                return tuple(model_outputs[0].get_shape().as_list())
        return tuple(model_outputs.get_shape().as_list())
    else:
        if isinstance(model_outputs, list):
            if len(model_outputs) > 1:
                return [tuple([batch_size] + list(output.get_shape().as_list()[1:])) for output in model_outputs]
            else:
                return tuple([batch_size] + list(model_outputs[0].get_shape().as_list()[1:]))
        return tuple([batch_size] + list(model_outputs.get_shape().as_list()[1:]))


def get_model_input(model, batch_size=None):
    model_inputs = model.inputs
    if batch_size is None:
        if isinstance(model_inputs, list):
            if len(model_inputs) > 1:
                return [tuple(inputs.get_shape().as_list()) for inputs in model_inputs]
            else:
                return tuple(model_inputs[0].get_shape().as_list())
        return tuple(model_inputs.get_shape().as_list())
    else:
        if isinstance(model_inputs, list):
            if len(model_inputs) > 1:
                return [tuple([batch_size] + list(output.get_shape().as_list()[1:])) for output in model_inputs]
            else:
                return tuple([batch_size] + list(model_inputs[0].get_shape().as_list()[1:]))
        return tuple([batch_size] + list(model_inputs.get_shape().as_list()[1:]))


def set_layer_name(layer, name):
    from keras.layers import Lambda
    if not isinstance(layer, list):
        layer = [layer]
    if isinstance(name, list):
        names = name
        layers = [Lambda(lambda x: x, name=names[i])(layer[i]) for i in range(len(layer))]
    else:
        layers = [Lambda(lambda x: x, name=name + '_%d' % i)(layer[i]) for i in range(len(layer))]
        names = [name + '_%d' % i for i, _ in enumerate(layers)]
    return layers, names


def listify(obj):
    if obj is None:
        return []
    return obj if isinstance(obj, list) else [obj]
