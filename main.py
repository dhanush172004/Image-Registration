def register_images(fixed_image, moving_image):
    fixed = sitk.GetImageFromArray(fixed_image.astype(np.float32))
    moving = sitk.GetImageFromArray(moving_image.astype(np.float32))

    registration = sitk.ImageRegistrationMethod()
    registration.SetMetricAsMeanSquares()
    registration.SetOptimizerAsRegularStepGradientDescent(learningRate=1.0,
                                                          minStep=0.01,
                                                          numberOfIterations=300)
    registration.SetInterpolator(sitk.sitkLinear)

    initial_transform = sitk.CenteredTransformInitializer(fixed, moving, sitk.AffineTransform(2),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registration.SetInitialTransform(initial_transform)

    final_transform = registration.Execute(fixed, moving)
    moving_resampled = sitk.Resample(moving, fixed, final_transform, sitk.sitkLinear, 0.0, moving.GetPixelID())

    return sitk.GetArrayFromImage(moving_resampled)

# Convert image to float before registration
registered_image = register_images(image.astype(np.float32), image.astype(np.float32))
plt.imshow(registered_image, cmap='gray')
plt.title("Registered Image")
plt.show()
