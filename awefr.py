import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the function to be plotted
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

# Generate the x and y values
x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

# Create a meshgrid
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, Z, cmap='viridis')

# Add labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot')

# Display the plot
plt.show()
